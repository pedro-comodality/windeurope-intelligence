from pyvis.network import Network


# =====================================================
# BUILD NETWORK GRAPH
# =====================================================

def build_network_graph(df):

    # =================================================
    # SAFE LIMIT
    # =================================================

    df = df.head(50)

    # =================================================
    # NETWORK
    # =================================================

    net = Network(

        height="900px",

        width="100%",

        bgcolor="#050B1A",

        font_color="white",

        notebook=False,

        directed=False

    )

    # =================================================
    # DISABLE PHYSICS
    # =================================================

    net.toggle_physics(False)

    # =================================================
    # ADD NODES
    # =================================================

    for _, row in df.iterrows():

        company = str(
            row.get("company", "Unknown")
        )

        # =============================================
        # SAFE SCORE
        # =============================================

        try:

            strategic_score = float(

                row.get(
                    "final_strategic_score",
                    50
                )

            )

        except:

            strategic_score = 50

        # =============================================
        # FLAGS
        # =============================================

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

        # =============================================
        # COLOR
        # =============================================

        color = "#4CAF50"

        if strategic == "ELITE":

            color = "#FF9800"

        elif floating:

            color = "#00BCD4"

        elif offshore:

            color = "#2196F3"

        # =============================================
        # SIZE
        # =============================================

        size = max(
            min(strategic_score / 4, 45),
            12
        )

        # =============================================
        # NODE
        # =============================================

        net.add_node(

            company,

            label=company,

            color=color,

            size=size,

            borderWidth=1,

            title=f"""
            <b>{company}</b><br>
            Strategic Score: {strategic_score}<br>
            Offshore: {offshore}<br>
            Floating: {floating}
            """

        )

    # =================================================
    # ADD EDGES
    # =================================================

    companies = df.to_dict("records")

    for i in range(len(companies)):

        c1 = companies[i]

        connections = 0

        for j in range(i + 1, len(companies)):

            if connections >= 4:
                break

            c2 = companies[j]

            score = 0

            # same segment

            if (
                c1.get("segmento")
                ==
                c2.get("segmento")
            ):

                score += 2

            # offshore

            if (
                str(c1.get("offshore")).lower()
                == "true"
                and
                str(c2.get("offshore")).lower()
                == "true"
            ):

                score += 2

            # floating

            if (
                str(c1.get("floating_wind")).lower()
                == "true"
                and
                str(c2.get("floating_wind")).lower()
                == "true"
            ):

                score += 3

            # epc

            if (
                str(c1.get("epc")).lower()
                == "true"
                and
                str(c2.get("epc")).lower()
                == "true"
            ):

                score += 1

            # =========================================
            # THRESHOLD
            # =========================================

            if score >= 4:

                net.add_edge(

                    str(c1.get("company")),

                    str(c2.get("company")),

                    color="#FFB300",

                    width=2

                )

                connections += 1

    # =================================================
    # OPTIONS
    # =================================================

    net.set_options("""
    {
      "nodes": {
        "font": {
          "size": 18
        }
      },
      "edges": {
        "smooth": false
      },
      "interaction": {
        "hover": true,
        "zoomView": true,
        "dragView": true
      }
    }
    """)

    return net.generate_html()