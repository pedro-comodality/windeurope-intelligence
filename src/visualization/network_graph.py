import pandas as pd
from pyvis.network import Network


# =====================================================
# SAFE BOOL
# =====================================================

def safe_bool(value):

    if pd.isna(value):
        return False

    return str(value).lower() in [
        "1",
        "true",
        "yes",
        "si"
    ]


# =====================================================
# BUILD NETWORK GRAPH
# =====================================================

def build_network_graph(df):

    # =================================================
    # LIMIT SIZE
    # =================================================

    df = df.sort_values(
        "final_strategic_score",
        ascending=False
    ).head(120)

    # =================================================
    # NETWORK
    # =================================================

    net = Network(

        height="950px",

        width="100%",

        bgcolor="#07111f",

        font_color="white",

        notebook=False
    )

    # =================================================
    # PHYSICS
    # =================================================

    net.barnes_hut(

        gravity=-12000,

        central_gravity=0.2,

        spring_length=180,

        spring_strength=0.02,

        damping=0.12
    )

    # =================================================
    # ADD NODES
    # =================================================

    for _, row in df.iterrows():

        company = str(
            row.get("company", "Unknown")
        )

        strategic = str(
            row.get(
                "strategic_category_v2",
                "NORMAL"
            )
        )

        offshore = safe_bool(
            row.get("offshore")
        )

        floating = safe_bool(
            row.get("floating_wind")
        )

        epc = safe_bool(
            row.get("epc")
        )

        digital = safe_bool(
            row.get("digitalizacion")
        )

        ai = safe_bool(
            row.get("ia")
        )

        country = str(
            row.get("country", "")
        )

        segment = str(
            row.get("segmento", "")
        )

        score = int(
            row.get(
                "final_strategic_score",
                50
            )
        )

        # =============================================
        # LOGISTICS SCORE
        # =============================================

        logistics_score = 0

        if offshore:
            logistics_score += 3

        if floating:
            logistics_score += 4

        if epc:
            logistics_score += 3

        if strategic == "ELITE":
            logistics_score += 3

        if score >= 80:
            logistics_score += 2

        # =============================================
        # COLORS
        # =============================================

        color = "#4CAF50"

        if floating:
            color = "#00BCD4"

        elif offshore:
            color = "#2196F3"

        elif epc:
            color = "#FF9800"

        elif ai:
            color = "#E91E63"

        # =============================================
        # NODE SIZE
        # =============================================

        node_size = max(
            int(score / 3),
            12
        )

        # =============================================
        # TOOLTIP
        # =============================================

        tooltip = f"""
        <b>{company}</b><br><br>

        <b>Country:</b> {country}<br>
        <b>Segment:</b> {segment}<br><br>

        <b>Strategic:</b> {strategic}<br>
        <b>Score:</b> {score}<br><br>

        <b>Offshore:</b> {offshore}<br>
        <b>Floating:</b> {floating}<br>
        <b>EPC:</b> {epc}<br>
        <b>AI:</b> {ai}<br><br>

        <b>LOGISTICS OPPORTUNITY:</b>
        {logistics_score}/15
        """

        # =============================================
        # ADD NODE
        # =============================================

        net.add_node(

            company,

            label=company,

            title=tooltip,

            color=color,

            size=node_size
        )

    # =================================================
    # RELATIONSHIPS
    # =================================================

    companies = df.to_dict("records")

    for i in range(len(companies)):

        for j in range(i + 1, len(companies)):

            c1 = companies[i]
            c2 = companies[j]

            score = 0

            # =========================================
            # SAME SEGMENT
            # =========================================

            if (
                c1.get("segmento")
                ==
                c2.get("segmento")
            ):

                score += 2

            # =========================================
            # BOTH OFFSHORE
            # =========================================

            if (
                safe_bool(c1.get("offshore"))
                and
                safe_bool(c2.get("offshore"))
            ):

                score += 3

            # =========================================
            # BOTH FLOATING
            # =========================================

            if (
                safe_bool(c1.get("floating_wind"))
                and
                safe_bool(c2.get("floating_wind"))
            ):

                score += 4

            # =========================================
            # BOTH EPC
            # =========================================

            if (
                safe_bool(c1.get("epc"))
                and
                safe_bool(c2.get("epc"))
            ):

                score += 3

            # =========================================
            # BOTH DIGITAL
            # =========================================

            if (
                safe_bool(c1.get("digitalizacion"))
                and
                safe_bool(c2.get("digitalizacion"))
            ):

                score += 1

            # =========================================
            # BOTH AI
            # =========================================

            if (
                safe_bool(c1.get("ia"))
                and
                safe_bool(c2.get("ia"))
            ):

                score += 2

            # =========================================
            # CONNECTION THRESHOLD
            # =========================================

            if score >= 5:

                edge_color = "#ffaa00"

                if score >= 8:
                    edge_color = "#00BCD4"

                net.add_edge(

                    str(c1.get("company")),

                    str(c2.get("company")),

                    value=score,

                    width=min(score, 10),

                    color=edge_color,

                    title=f"""
                    Relationship Strength:
                    {score}
                    """
                )

    # =================================================
    # OPTIONS
    # =================================================

    net.set_options("""
    var options = {

      "nodes": {

        "font": {
          "size": 14,
          "color": "white"
        },

        "borderWidth": 1
      },

      "edges": {

        "smooth": {
          "type": "dynamic"
        }
      },

      "interaction": {

        "hover": true,

        "navigationButtons": true,

        "keyboard": true
      },

      "physics": {

        "enabled": true
      }
    }
    """)

    return net.generate_html()