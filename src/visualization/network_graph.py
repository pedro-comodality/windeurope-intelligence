from pyvis.network import Network


def build_network_graph(df):

    # LIMIT
    df = df.head(50)

    net = Network(

        height="900px",
        width="100%",
        bgcolor="#050B1A",
        font_color="white",
        notebook=False

    )

    # IMPORTANT
    net.toggle_physics(False)

    # NODES
    for _, row in df.iterrows():

        company = str(
            row.get("company", "Unknown")
        )

        color = "#4CAF50"

        offshore = str(
            row.get("offshore", "")
        ).lower() == "true"

        floating = str(
            row.get("floating_wind", "")
        ).lower() == "true"

        strategic = str(
            row.get(
                "strategic_category_v2",
                "NORMAL"
            )
        )

        if strategic == "ELITE":

            color = "#FF9800"

        elif floating:

            color = "#00BCD4"

        elif offshore:

            color = "#2196F3"

        try:

            size = float(
                row.get(
                    "final_strategic_score",
                    50
                )
            ) / 4

        except:

            size = 15

        size = max(size, 12)

        net.add_node(

            company,

            label=company,

            color=color,

            size=size,

            title=f"""
            {company}
            """

        )

    # EDGES
    companies = df.to_dict("records")

    for i in range(len(companies)):

        c1 = companies[i]

        added = 0

        for j in range(i + 1, len(companies)):

            if added >= 3:
                break

            c2 = companies[j]

            score = 0

            if c1.get("segmento") == c2.get("segmento"):
                score += 2

            if (
                str(c1.get("offshore")).lower() == "true"
                and
                str(c2.get("offshore")).lower() == "true"
            ):
                score += 2

            if (
                str(c1.get("floating_wind")).lower() == "true"
                and
                str(c2.get("floating_wind")).lower() == "true"
            ):
                score += 3

            if score >= 4:

                net.add_edge(

                    str(c1.get("company")),

                    str(c2.get("company")),

                    color="#FFB300",

                    width=2

                )

                added += 1

    return net.generate_html()