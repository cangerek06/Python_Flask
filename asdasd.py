import ast

"""Data = {1:{
        "encoding":"encoding_verisi",
        "seen_frames":[1, 2, 3, 4],
        "ratio_points":[1.22, 1.23, 1.22, 2.11],
        "match_points":[11.22, 23.11, 11.22, 23.11],
        "video_token":["K123CKOPS"],
        "identifier":["1K123CKOPS"]

        },
        2:{
        "encoding":"encoding_verisi",
        "seen_frames":[1, 2, 3, 4],
        "ratio_points":[1.22, 1.23, 1.22, 2.11],
        "match_points":[11.22, 23.11, 11.22, 23.11],
        "video_token":["K123CKOPS"],
        "identifier":["1K123CKOPS"]

        }}

for i in Data:
    print(i)"""


liste = "{1,2,3,4,5}"
liste2 = liste[1:-1]
liste2 = list(liste2.split(","))
print(liste2)
