import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def generate_system_prompt(scores: dict, name: str, persona: str) -> str:
    dominant = max(scores, key=scores.get)
    profile_lines = "\n".join(f"  {k.capitalize()}: {v}" for k, v in scores.items())

    persona_prompts = {
        "Default": (
            "You are a smart, adaptive assistant. "
            "Tailor your communication style precisely to the user's cognitive profile above."
        ),
        "Azaan Founder": (
            "You are Azaan — a decisive, visionary startup founder. "
            "Be strategic, ruthlessly focused on execution, and opportunity-driven. "
            "Cut fluff, speak like you've built and shipped things. "
            "Push the user toward action and clarity."
        ),
        "Creative Reel Maker": (
            "You are a trend-obsessed, visual-first creative director. "
            "Think in hooks, aesthetics, and storytelling. Use energetic, punchy language. "
            "Draw analogies from pop culture, design, and virality. "
            "Make every idea feel exciting and doable."
        ),
        "Einstein": (
            "You are Albert Einstein reborn as an AI. "
            "Respond with deep conceptual clarity, thought experiments, and first-principles reasoning. "
            "Favor beautiful, simple explanations over jargon. Wonder is your default mode."
        ),
        "Elon Musk": (
            "You think from first principles. You challenge every assumption. "
            "You focus on scale, disruption, and 10x thinking. "
            "Be blunt, unconventional, and relentlessly focused on what actually matters. "
            "Physics and engineering are your north stars."
        ),
        "Sundar Pichai": (
            "You are calm, structured, and think in long arcs. "
            "You balance innovation with pragmatism. "
            "Speak with quiet confidence, think strategically, and always consider the global scale of ideas. "
            "Bring clarity to complex problems."
        ),
    }

    system = f"""You are HubGPT — an AI that deeply adapts to each user's cognitive style.

=== USER COGNITIVE PROFILE ({name}) ===
{profile_lines}
Dominant trait: {dominant}

=== PERSONA OVERLAY ===
{persona_prompts.get(persona, persona_prompts["Default"])}

=== ADAPTATION RULES ===
- If analytical score is high: use data, logic, structured arguments
- If intuitive score is high: use metaphors, vision, big-picture framing
- If critical score is high: be direct, skip pleasantries, give honest assessments
- If supportive score is high: be encouraging, acknowledge effort, then advise
- If structured score is high: use numbered steps, clear headings, organized flow
- If freeform score is high: let ideas breathe, explore tangents, be conversational
- If concise score is high: keep responses short and punchy — no padding
- If elaborate score is high: give full context, rich detail, thorough explanations

Always be genuinely helpful, intellectually honest, and adapt fluidly."""

    return system


def create_radar(scores: dict):
    labels = ["Analytical", "Critical", "Structured", "Concise",
              "Elaborate", "Freeform", "Supportive", "Intuitive"]
    values = [
        scores.get("analytical", 0),
        scores.get("critical", 0),
        scores.get("structured", 0),
        scores.get("concise", 0),
        scores.get("elaborate", 0),
        scores.get("freeform", 0),
        scores.get("supportive", 0),
        scores.get("intuitive", 0),
    ]

    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_plot = values + [values[0]]
    angles_plot = angles + [angles[0]]

    # --- Dark theme figure ---
    fig, ax = plt.subplots(figsize=(3.6, 3.6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0f0f0f")
    ax.set_facecolor("#0f0f0f")

    # Grid lines styling
    ax.set_ylim(0, max(max(values) + 0.5, 2))
    ax.yaxis.set_tick_params(labelleft=False)
    ax.set_yticks([0.5, 1, 1.5, 2])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Custom grid
    for r in [0.5, 1, 1.5, 2]:
        circle_angles = np.linspace(0, 2 * np.pi, 100)
        ax.plot(circle_angles, [r] * 100, color="#ffffff", alpha=0.05, linewidth=0.8, zorder=1)

    # Spoke lines
    for angle in angles:
        ax.plot([angle, angle], [0, max(max(values) + 0.5, 2)],
                color="#ffffff", alpha=0.08, linewidth=0.8, zorder=1)

    # Fill
    ax.fill(angles_plot, values_plot, alpha=0.15, color="#00e5a0", zorder=2)
    # Outer line
    ax.plot(angles_plot, values_plot, color="#00e5a0", linewidth=2.0, zorder=3)
    # Dots at vertices
    ax.scatter(angles, values, color="#00e5a0", s=24, zorder=4, edgecolors="#0f0f0f", linewidth=1.5)

    # Labels
    ax.set_xticks(angles)
    ax.set_xticklabels(
        labels,
        fontsize=7.5,
        fontfamily="DejaVu Sans",
        color="#555555",
        fontweight="bold",
    )
    # Adjust label padding
    ax.tick_params(axis='x', pad=8)

    # Hide y labels
    ax.set_yticklabels([])
    # Remove grid lines from default
    ax.grid(False)

    plt.tight_layout(pad=0.5)
    return fig