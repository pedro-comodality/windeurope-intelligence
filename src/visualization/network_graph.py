import networkx as nx

from pyvis.network import Network


# =====================================================
# BUILD GRAPH
# =====================================================

def build_network_graph(df):

    net = Network(
        height="900px",
        width="100%",
        bgcolor="#111111",
        font_color="white"
    )

    G = nx.Graph()

    # =================================================
    # ADD COMPANY NODES
    # =================================================

    for _, row in df.iterrows():

        company = row.get("company", "")

        strategic = row.get(
            "strategic_level",
            ""
        )

        offshore = row.get(
            "offshore",
            False
        )

        floating = row.get(
            "floating_wind",
            False
        )

        # color logic

        color = "#4CAF50"

        if strategic == "STRATEGIC":
            color = "#FF9800"

        elif floating:
            color = "#00BCD4"

        elif offshore:
            color = "#2196F3"

        G.add_node(
            company,
            title=f"""
Company: {company}
Strategic: {strategic}
Offshore: {offshore}
Floating: {floating}
""",
            color=color
        )

    # =================================================
    # CREATE RELATIONSHIPS
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

            # both offshore
            if c1.get("offshore") and c2.get("offshore"):
                score += 1

            # both floating
            if c1.get("floating_wind") and c2.get("floating_wind"):
                score += 2

            # both EPC
            if c1.get("epc") and c2.get("epc"):
                score += 1

            # connection threshold
            if score >= 2:

                G.add_edge(
                    c1["company"],
                    c2["company"],
                    value=score
                )

    net.from_nx(G)

    net.force_atlas_2based()

    output_path = (
        "dashboard/network_graph.html"
    )

    net.save_graph(output_path)

    return output_path