"""Utility to visualize photo plans.
"""

import math
import typing as T

import plotly.graph_objects as go
import plotly.io as pio

from src.data_model import Waypoint


def plot_photo_plan(photo_plans: T.List[Waypoint]) -> go.Figure:
    """Plot the photo plan on a 2D grid.

    Args:
        photo_plans: List of waypoints for the photo plan.

    Returns:
        Plotly figure object.
    """
    xs = [wp.x for wp in photo_plans]
    ys = [wp.y for wp in photo_plans]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="lines+markers",
        name="Waypoints",
        marker=dict(size=6),
    ))

    fig.update_layout(
        title="Drone Photo Plan",
        xaxis_title="X (m)",
        yaxis_title="Y (m)",
        yaxis_scaleanchor="x",
    )

    return fig


def plot_photo_plan_dashboard(photo_plans: T.List[Waypoint]) -> go.Figure:
    """Plot a polished dark-theme dashboard with gradient coloring and flight stats.

    Args:
        photo_plans: List of waypoints for the photo plan.

    Returns:
        Plotly figure object.
    """
    xs = [wp.x for wp in photo_plans]
    ys = [wp.y for wp in photo_plans]
    n = len(photo_plans)
    indices = list(range(n))

    total_dist = sum(
        math.sqrt((xs[i] - xs[i-1])**2 + (ys[i] - ys[i-1])**2)
        for i in range(1, n)
    )
    speed = photo_plans[0].speed if photo_plans else 0
    est_time_min = (total_dist / speed / 60) if speed > 0 else 0

    fig = go.Figure()

    # Path with gradient color by waypoint order
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="lines+markers",
        marker=dict(
            size=9,
            color=indices,
            colorscale="Plasma",
            showscale=True,
            colorbar=dict(
                title=dict(text="Waypoint #", font=dict(size=14, color="white")),
                thickness=20,
                tickfont=dict(color="white", size=13),
                len=0.75,
            ),
        ),
        line=dict(color="rgba(255,255,255,0.2)", width=1.5),
        name="Flight Path",
        hovertemplate="WP %{marker.color}<br>x: %{x:.1f}m<br>y: %{y:.1f}m<extra></extra>",
    ))

    # Start marker
    fig.add_trace(go.Scatter(
        x=[xs[0]], y=[ys[0]],
        mode="markers+text",
        marker=dict(size=18, color="lime", symbol="circle"),
        text=["START"], textposition="top center",
        textfont=dict(color="lime", size=15),
        name="Start",
    ))

    # End marker
    fig.add_trace(go.Scatter(
        x=[xs[-1]], y=[ys[-1]],
        mode="markers+text",
        marker=dict(size=18, color="red", symbol="x"),
        text=["END"], textposition="top center",
        textfont=dict(color="red", size=15),
        name="End",
    ))

    fig.update_layout(
        template="plotly_dark",
        title=dict(text="Drone Flight Plan", font=dict(size=28, color="white"), x=0.5),
        xaxis=dict(
            title=dict(text="X (m)", font=dict(size=16)),
            tickfont=dict(size=14),
        ),
        yaxis=dict(
            title=dict(text="Y (m)", font=dict(size=16)),
            tickfont=dict(size=14),
        ),
        legend=dict(font=dict(size=14)),
        autosize=True,
        height=820,
        margin=dict(l=80, r=40, t=80, b=80),
        paper_bgcolor="#0d0d0d",
        plot_bgcolor="#0d0d0d",
        annotations=[dict(
            name="stats",
            x=0.01, y=0.99,
            xref="paper", yref="paper",
            text=(
                f"<b>Waypoints:</b> {n}<br><br>"
                f"<b>Total Distance:</b> {total_dist:.0f} m<br><br>"
                f"<b>Capture Speed:</b> {speed:.2f} m/s<br><br>"
                f"<b>Est. Flight Time:</b> {est_time_min:.1f} min"
            ),
            showarrow=False,
            align="left",
            bgcolor="rgba(0,0,0,0.7)",
            bordercolor="cyan",
            borderwidth=1,
            borderpad=12,
            font=dict(size=15, color="white"),
            visible=True,
        )],
        updatemenus=[dict(
            type="buttons",
            showactive=True,
            active=0,
            x=0.01, y=1.2,
            xanchor="left",
            yanchor="top",
            bgcolor="#0d0d0d",
            bordercolor="#00d4ff",
            font=dict(color="#00d4ff", size=12),
            buttons=[
                dict(
                    label="▼ Hide Stats",
                    method="relayout",
                    args=[{"annotations[0].visible": False}],
                ),
                dict(
                    label="▶ Show Stats",
                    method="relayout",
                    args=[{"annotations[0].visible": True}],
                ),
            ],
        )],
    )

    return fig


def plot_photo_plan_animated(
    photo_plans: T.List[Waypoint], frame_step: int = 1
) -> go.Figure:
    """Animate the drone flying along the flight plan waypoint by waypoint.

    Args:
        photo_plans: List of waypoints for the photo plan.
        frame_step: Number of waypoints to advance per frame. Increase for faster animation.

    Returns:
        Plotly figure object with animation controls.
    """
    xs = [wp.x for wp in photo_plans]
    ys = [wp.y for wp in photo_plans]
    n = len(photo_plans)

    steps = list(range(1, n + 1, frame_step))
    if steps[-1] != n:
        steps.append(n)

    frames = []
    for i in steps:
        frames.append(go.Frame(
            data=[
                go.Scatter(
                    x=xs[:i], y=ys[:i],
                    mode="lines",
                    line=dict(color="cyan", width=2),
                    name="Path",
                ),
                go.Scatter(
                    x=[xs[i-1]], y=[ys[i-1]],
                    mode="markers",
                    marker=dict(size=14, color="yellow", symbol="triangle-up"),
                    name="Drone",
                ),
            ],
            name=str(i),
        ))

    fig = go.Figure(
        data=[
            go.Scatter(
                x=[xs[0]], y=[ys[0]],
                mode="lines",
                line=dict(color="cyan", width=2),
                name="Path",
            ),
            go.Scatter(
                x=[xs[0]], y=[ys[0]],
                mode="markers",
                marker=dict(size=14, color="yellow", symbol="triangle-up"),
                name="Drone",
            ),
        ],
        frames=frames,
    )

    fig.update_layout(
        template="plotly_dark",
        title=dict(text="Drone Flight Simulation", font=dict(size=28, color="white"), x=0.5),
        xaxis=dict(
            title=dict(text="X (m)", font=dict(size=16)),
            tickfont=dict(size=14),
            range=[min(xs) - 10, max(xs) + 10],
        ),
        yaxis=dict(
            title=dict(text="Y (m)", font=dict(size=16)),
            tickfont=dict(size=14),
            range=[min(ys) - 10, max(ys) + 10],
            scaleanchor="x",
        ),
        legend=dict(font=dict(size=14)),
        autosize=True,
        height=820,
        margin=dict(l=80, r=40, t=80, b=120),
        paper_bgcolor="#0d0d0d",
        plot_bgcolor="#0d0d0d",
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            y=0,
            x=0.5,
            xanchor="center",
            yanchor="top",
            buttons=[
                dict(
                    label="▶  Play",
                    method="animate",
                    args=[None, dict(frame=dict(duration=80, redraw=True), fromcurrent=True)],
                ),
                dict(
                    label="⏸  Pause",
                    method="animate",
                    args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")],
                ),
            ],
        )],
        sliders=[dict(
            steps=[
                dict(
                    method="animate",
                    args=[[str(i)], dict(mode="immediate", frame=dict(duration=0))],
                    label=str(i),
                )
                for i in steps
            ],
            x=0.05, y=0, len=0.9,
            currentvalue=dict(prefix="Waypoint: ", font=dict(size=13, color="white")),
            font=dict(color="white"),
        )],
    )

    return fig


def build_presentation_html(plans: T.Dict[str, T.List[Waypoint]]) -> str:
    """Build a standalone presentation HTML page with all patterns and both views.

    Args:
        plans: dict mapping pattern name ('grid', 'spiral', 'zigzag') to waypoint list.

    Returns:
        Full HTML string ready to write to a file.
    """
    plot_divs = ""
    for pattern_name, plan in plans.items():
        for view_name, fig in [
            ("dashboard", plot_photo_plan_dashboard(plan)),
            ("animated", plot_photo_plan_animated(plan)),
        ]:
            div = pio.to_html(fig, full_html=False, include_plotlyjs=False)
            plot_divs += f'<div class="plot-panel" id="{pattern_name}-{view_name}">{div}</div>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Drone Trajectory Planner</title>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: #08080f;
      color: #fff;
      font-family: 'Segoe UI', system-ui, sans-serif;
      min-height: 100vh;
    }}
    header {{
      padding: 2rem 3rem 1.5rem;
      background: linear-gradient(135deg, #0d0d1a 0%, #0a1628 100%);
      border-bottom: 1px solid #1e3a5f;
    }}
    h1 {{
      font-size: 2rem;
      color: #00d4ff;
      letter-spacing: 3px;
      text-transform: uppercase;
      font-weight: 300;
    }}
    .subtitle {{
      color: #556677;
      margin-top: 0.4rem;
      font-size: 0.88rem;
      letter-spacing: 1px;
    }}
    .controls {{
      display: flex;
      gap: 2rem;
      padding: 1.2rem 3rem;
      background: #0d0d1a;
      border-bottom: 1px solid #151f2e;
      align-items: center;
      flex-wrap: wrap;
    }}
    .control-group {{ display: flex; gap: 0.4rem; align-items: center; }}
    .control-label {{
      color: #445566;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-right: 0.5rem;
    }}
    .divider {{ width: 1px; background: #1e3a5f; height: 28px; }}
    button.tab {{
      padding: 0.45rem 1.1rem;
      border: 1px solid #1e3a5f;
      background: transparent;
      color: #667788;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.85rem;
      letter-spacing: 0.5px;
      transition: all 0.15s;
    }}
    button.tab:hover {{ border-color: #00d4ff; color: #00d4ff; }}
    button.tab.active {{
      background: #00d4ff;
      color: #000;
      border-color: #00d4ff;
      font-weight: 600;
    }}
    .plot-wrapper {{ padding: 1.5rem 2rem; }}
    .plot-panel {{ display: none; width: 100%; }}
    .plot-panel.active {{ display: block; width: 100%; }}
    .plot-panel .js-plotly-plot,
    .plot-panel .plotly {{ width: 100% !important; }}
    footer {{
      text-align: center;
      padding: 1.2rem;
      color: #334455;
      font-size: 0.78rem;
      border-top: 1px solid #151f2e;
      letter-spacing: 1px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>&#x1F6F8;&nbsp; Drone Trajectory Planner</h1>
    <p class="subtitle">Skydio X10 &nbsp;·&nbsp; 70% overlap / 70% sidelap &nbsp;·&nbsp; 30m altitude &nbsp;·&nbsp; 150 × 150 m scan area</p>
  </header>

  <div class="controls">
    <div class="control-group" id="pattern-group">
      <span class="control-label">Pattern</span>
      <button class="tab active" onclick="setPattern('grid', this)">Grid</button>
      <button class="tab" onclick="setPattern('spiral', this)">Spiral</button>
      <button class="tab" onclick="setPattern('zigzag', this)">Zigzag</button>
    </div>
    <div class="divider"></div>
    <div class="control-group" id="view-group">
      <span class="control-label">View</span>
      <button class="tab active" onclick="setView('dashboard', this)">Dashboard</button>
      <button class="tab" onclick="setView('animated', this)">Simulation</button>
    </div>
  </div>

  <div class="plot-wrapper">
    {plot_divs}
  </div>

  <footer>Drone Trajectory Planner &nbsp;·&nbsp; CS Spring 2026</footer>

  <script>
    let currentPattern = 'grid';
    let currentView = 'dashboard';

    function updateVisible() {{
      document.querySelectorAll('.plot-panel').forEach(el => el.classList.remove('active'));
      const el = document.getElementById(currentPattern + '-' + currentView);
      if (el) el.classList.add('active');
    }}

    function setPattern(pattern, btn) {{
      currentPattern = pattern;
      document.querySelectorAll('#pattern-group .tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      updateVisible();
    }}

    function setView(view, btn) {{
      currentView = view;
      document.querySelectorAll('#view-group .tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      updateVisible();
    }}

    updateVisible();

    function resizePlots() {{
      document.querySelectorAll('.js-plotly-plot').forEach(function(div) {{
        Plotly.relayout(div, {{width: div.parentElement.offsetWidth}});
      }});
    }}

    window.addEventListener('load', resizePlots);
    window.addEventListener('resize', resizePlots);
  </script>
</body>
</html>"""
