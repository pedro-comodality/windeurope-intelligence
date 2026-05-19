import networkx as nx

from pyvis.network import Network


# =====================================================
# SAFE BOOL
# =====================================================

def safe_bool(value):

    return str(value).lower() in [

        "true",
        "1",
        "yes",
        "y"

    ]


# =====================================================
# BUILD NETWORK GRAPH
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
    # ADD NODES
    # =================================================

    for _, row in df.iterrows():

        company = str(
            row.get("company", "")
        )

        if not company:
            continue

        strategic = str(
            row.get(
                "strategic_category_v2",
                ""
            )
        )

        offshore = safe_bool(
            row.get("offshore", False)
        )

        floating = safe_bool(
            row.get("floating_wind", False)
        )

        # =============================================
        # COLOR LOGIC
        # =============================================

        color = "#4CAF50"

        if strategic == "ELITE":

            color = "#FF5252"

        elif strategic == "STRATEGIC":

            color = "#FF9800"

        elif floating:

            color = "#00BCD4"

        elif offshore:

            color = "#2196F3"

        # =============================================
        # ADD NODE
        # =============================================

        G.add_node(

            company,

            title=f"""
Company: {company}
Strategic: {strategic}
Offshore: {offshore}
Floating: {floating}
""",

            color=color,

            size=20

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

            if str(
                c1.get("segmento", "")
            ) == str(
                c2.get("segmento", "")
            ):

                score += 1

            # =========================================
            # OFFSHORE
            # =========================================

            if safe_bool(
                c1.get("offshore")
            ) and safe_bool(
                c2.get("offshore")
            ):

                score += 1

            # =========================================
            # FLOATING
            # =========================================

            if safe_bool(
                c1.get("floating_wind")
            ) and safe_bool(
                c2.get("floating_wind")
            ):

                score += 2

            # =========================================
            # EPC
            # =========================================

            if safe_bool(
                c1.get("epc")
            ) and safe_bool(
                c2.get("epc")
            ):

                score += 1

            # =========================================
            # EDGE
            # =========================================

            if score >= 2:

                G.add_edge(

                    str(c1.get("company")),

                    str(c2.get("company")),

                    value=score

                )

    # =================================================
    # LOAD NETWORK
    # =================================================

    net.from_nx(G)

    net.force_atlas_2based()

    # =================================================
    # SAVE
    # =================================================

    output_path = (
        "dashboard/network_graph.html"
    )

    net.save_graph(output_path)

    return output_path