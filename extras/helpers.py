from __future__ import annotations

import warnings

import matplotlib.pyplot as plt
import numpy as np
import xtrack as xt

# ----- Plotting helpers ----- #


def arrange_phase_space_plot():
    """
    Generates a layout for plotting phase space in both physical and normalized coordinates.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object containing the subplots.
    ax_geom : matplotlib.axes.Axes
        The axis for the physical phase space plot.
    ax_norm : matplotlib.axes.Axes
        The axis for the normalized phase space plot.
    """
    fig, (ax_geom, ax_norm) = plt.subplots(1, 2, figsize=(10, 5), layout="tight")
    ax_geom.set_title("Espace des phases physique")
    ax_norm.set_title("Espace des phases normalisé")
    ax_geom.set_xlim(-5e-2, 5e-2)
    ax_geom.set_ylim(-5e-3, 5e-3)
    ax_norm.set_xlim(-15e-3, 15e-3)
    ax_norm.set_ylim(-15e-3, 15e-3)
    ax_geom.set_xlabel(r"${x}$ [m]")
    ax_geom.set_ylabel(r"${p}_x$")
    ax_norm.set_xlabel(r"$\hat{x}$")
    ax_norm.set_ylabel(r"$\hat{p}_x$")
    for axis in (ax_geom, ax_norm):
        axis.xaxis.set_major_locator(plt.MaxNLocator(5))
        axis.yaxis.set_major_locator(plt.MaxNLocator(5))

    return fig, ax_geom, ax_norm


# ----- Phase space characterization ----- #


def characterize_phase_space(line: xt.Line, plot: bool = True) -> dict[str, float | np.ndarray]:
    """
    Characterizes the phase space of a beam in both physical and
    normalized coordinates. Optionally plots the phase space in
    both coordinate systems. This function essentially repeats
    the from the notebook '03_characterisation_espace_phase.ipynb',
    look into there for details. A third order resonance is assumed.

    Parameters
    ----------
    line : xt.Line
        The accelerator line to be analyzed.
    plot : bool, optional
        Whether to plot the phase space, by default True.

    Returns
    -------
    dict[str, float | np.ndarray]
        A dictionary containing the following keys:
        - 'stable_area': Area of the stable region in normalized coordinates.
        - 'dpx_dx_at_septum': Slope of the separatrix at the septum location.
        - 'x_fixed_points': x-coordinates of the fixed points in physical space.
        - 'px_fixed_points': px-coordinates of the fixed points in physical space.
        - 'x_norm_fixed_points': x-coordinates of the fixed points in normalized space.
        - 'px_norm_fixed_points': px-coordinates of the fixed points in normalized space.
    """
    # ---------------------------------------------------------------
    # Twiss the line and define some hardcoded properties
    twiss: xt.TwissTable = line.twiss4d()  # no need for 6D
    x_septum: float = 3.5e-2
    num_turns: int = 1000
    # ---------------------------------------------------------------
    # We start by just getting the phase space itself by tracking
    x_gen = np.linspace(0, 2.5e-2, 25)
    parts = line.build_particles(x=x_gen, px=0, y=0, py=0, zeta=0, delta=0)
    line.track(parts, num_turns=1000, turn_by_turn_monitor=True)
    record = line.record_last_track
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        norm_coords = twiss.get_normalized_coordinates(record)
    # ---------------------------------------------------------------
    # Now let's binary search for the separatrix via tracking
    x_stable, x_unstable = 0, 0.03
    while x_unstable - x_stable > 1e-6:
        x_test = (x_stable + x_unstable) / 2
        p = line.build_particles(x=x_test, px=0)
        line.track(p, num_turns=num_turns, turn_by_turn_monitor=True)
        rec_test = line.record_last_track
        # Update the search region after tracking
        if (rec_test.x > x_septum).any():  # Unstable part, separatrix is on the right of x_test
            x_unstable = x_test
        else:  # Stable part, separatrix is on the left of x_test
            x_stable = x_test
    # ---------------------------------------------------------------
    # Track a particle juuust beyond the limit of stability
    # will give us a good approximation of the separatrix
    p = line.build_particles(x=x_unstable, px=0)
    line.track(p, num_turns=num_turns, turn_by_turn_monitor=True)
    rec_separatrix = line.record_last_track
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        norm_separatrix = twiss.get_normalized_coordinates(rec_separatrix)
    # ---------------------------------------------------------------
    # Get the separatrix slope at the septum location
    x_separ, px_separ = rec_separatrix.x[0, :], rec_separatrix.px[0, :]
    i_septum: int = np.argmin(np.abs(x_separ - x_septum))
    lims_x_separ = [x_separ[i_septum - 3], x_separ[i_septum + 3]]
    lims_px_separ = [px_separ[i_septum - 3], px_separ[i_septum + 3]]
    poly_sep = np.polyfit(lims_x_separ, lims_px_separ, deg=1)
    dpx_dx_at_septum: float = poly_sep[0]
    # ---------------------------------------------------------------
    # Identify stable area by tracking a particle just bellow the limit of stability
    p = line.build_particles(x=x_stable, px=0)
    line.track(p, num_turns=num_turns, turn_by_turn_monitor=True)
    rec_triangle = line.record_last_track
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        nc_triangle = twiss.get_normalized_coordinates(rec_triangle)
    x_triangle = rec_triangle.x[0, :]
    px_triangle = rec_triangle.px[0, :]
    x_norm_triangle = nc_triangle.x_norm[0, :]
    px_norm_triangle = nc_triangle.px_norm[0, :]
    theta_triangle = np.angle(x_norm_triangle + 1j * px_norm_triangle)
    i_sorted = np.argsort(theta_triangle)
    x_triangle = x_triangle[i_sorted]
    px_triangle = px_triangle[i_sorted]
    x_norm_triangle = x_norm_triangle[i_sorted]
    px_norm_triangle = px_norm_triangle[i_sorted]
    # ---------------------------------------------------------------
    # Identify the fixed points in both coordinate systems
    z_triangle = rec_triangle.x[0, :] + 1j * rec_triangle.px[0, :]
    z_triangle_norm = nc_triangle.x_norm[0, :] + 1j * nc_triangle.px_norm[0, :]
    r_triangle_norm = np.abs(z_triangle_norm)
    i_fp1 = np.argmax(r_triangle_norm)
    z_fp1 = z_triangle_norm[i_fp1]
    r_fp1 = np.abs(z_fp1)
    mask_fp2 = np.abs(z_triangle_norm - z_fp1 * np.exp(1j * 2 / 3 * np.pi)) < 0.2 * r_fp1
    i_fp2 = np.argmax(r_triangle_norm * mask_fp2)
    mask_fp3 = np.abs(z_triangle_norm - z_fp1 * np.exp(-1j * 2 / 3 * np.pi)) < 0.2 * r_fp1
    i_fp3 = np.argmax(r_triangle_norm * mask_fp3)
    x_fp = z_triangle[[i_fp1, i_fp2, i_fp3]].real
    px_fp = z_triangle[[i_fp1, i_fp2, i_fp3]].imag
    x_norm_fp = z_triangle_norm[[i_fp1, i_fp2, i_fp3]].real
    px_norm_fp = z_triangle_norm[[i_fp1, i_fp2, i_fp3]].imag
    # ---------------------------------------------------------------
    # Compute the stable region area
    stable_area = np.linalg.det([x_norm_fp, px_norm_fp, [1, 1, 1]])
    # ---------------------------------------------------------------
    # Plot the phase space with all this info if requested
    if plot is True:
        fig, ax_geom, ax_norm = arrange_phase_space_plot()
        ymin, ymax = ax_geom.get_ylim()
        ax_geom.plot(record.x.T, record.px.T, ".", markersize=1, color="C0")
        ax_norm.plot(norm_coords.x_norm.T, norm_coords.px_norm.T, ".", markersize=1, color="C0")
        ax_geom.axvline(x=x_septum, color="k", alpha=0.4, linestyle="--")
        ax_geom.text(
            x_septum * 0.98, ymax * 0.95, "Septum", rotation=90, va="top", ha="right", alpha=0.5, c="k"
        )
        # Add the determined separatrix
        mask_alive = rec_separatrix.state > 0
        for ii in range(3):
            ax_geom.plot(
                rec_separatrix.x[mask_alive][ii::3],
                rec_separatrix.px[mask_alive][ii::3],
                "-",
                lw=2,
                color="C1",
                alpha=0.9,
            )
            ax_norm.plot(
                norm_separatrix.x_norm[mask_alive][ii::3],
                norm_separatrix.px_norm[mask_alive][ii::3],
                "-",
                lw=2,
                color="C1",
                alpha=0.9,
            )
        # Add the separatrix slope at the septum
        intervale_x_pente = [x_septum - 1e-2, x_septum + 1e-2]
        ax_geom.plot(intervale_x_pente, np.polyval(poly_sep, intervale_x_pente), "--k", linewidth=2)
        # Add the limits of the stable triangle
        ax_geom.plot(x_triangle, px_triangle, "-", lw=2, color="C2", alpha=0.9)
        ax_norm.plot(x_norm_triangle, px_norm_triangle, "-", lw=2, color="C2", alpha=0.9)
        # Add the fixed points
        ax_geom.plot(x_fp, px_fp, "*", markersize=10, color="k")
        ax_norm.plot(x_norm_fp, px_norm_fp, "*", markersize=10, color="k")
        plt.tight_layout()
    # ---------------------------------------------------------------
    # Return the values of interest in a dictionary
    return {
        "stable_area": stable_area,
        "dpx_dx_at_septum": dpx_dx_at_septum,
        "x_fixed_points": x_fp,
        "px_fixed_points": px_fp,
        "x_norm_fixed_points": x_norm_fp,
        "px_norm_fixed_points": px_norm_fp,
    }
