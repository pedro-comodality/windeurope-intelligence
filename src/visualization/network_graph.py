import networkx as nx
from pyvis.network import Network


# =====================================================
# BUILD NETWORK GRAPH
# =====================================================

def build_network_graph(df):

    net = Network(
        height="800px",
        width="100%",
        bgcolor="#0E1117",
        font_color="white",
        notebook=False
    )

    # physics
    net.barnes_hut()

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

        offshore = bool(
            row.get("offshore", False)
        )

        floating = bool(
            row.get("floating_wind", False)
        )

        # =============================================
        # COLOR LOGIC
        # =============================================

        color = "#4CAF50"

        if strategic == "ELITE":
            color = "#FF9800"

        elif floating:
            color = "#00BCD4"

        elif offshore:
            color = "#2196F3"

        net.add_node(
            company,
            label=company,
            color=color,
            title=f"""
            <b>{company}</b><br>
            Strategic: {strategic}<br>
            Offshore: {offshore}<br>
            Floating: {floating}
            """
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

            # same segment
            if c1.get("segmento") == c2.get("segmento"):
                score += 1

            # offshore
            if c1.get("offshore") and c2.get("offshore"):
                score += 1

            # floating
            if c1.get("floating_wind") and c2.get("floating_wind"):
                score += 2

            # epc
            if c1.get("epc") and c2.get("epc"):
                score += 1

            # threshold
            if score >= 2:

                net.add_edge(
                    str(c1.get("company")),
                    str(c2.get("company")),
                    value=score
                )

    # =================================================
    # RETURN HTML
    # =================================================

    html = net.generate_html()

    print("HTML GENERATED")

    print(len(html))

    return html