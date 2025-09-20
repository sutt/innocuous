# innocuous \
#     --initial-prompt-text "A great place to visit in boston is" \
#     --chunk-size 2 \
#     -vv \
#     encode \
#     --text "hey"

# A great place to visit in boston is  The New England Aquarium is a must for anyone interested in marine life. With various exhibits showcasing different

innocuous \
    --initial-prompt-text "A great place to visit in boston is the New England Aquarium." \
    --chunk-size 2 \
    --num-logprobs 100 \
    -vv \
    --log-file ./tests/data/recorded-logits/visit-boston-1.log \
    encode \
    --text "hey"

# A great place to visit in boston is the New England Aquarium. The Aquarium is a world leader in ocean exploration and marine conservation research. They have over a thousand animals and a wide

# logfile:
# {
#     "0": {
#         "top_logits": {
#             " It": 0.29587915539741516,
#             " The": 0.2691734731197357,
#             " This": 0.18136197328567505,
#             " Loc": 0.03182906284928322,
#             " Here": 0.029549943283200264,
#             " I": 0.02933475188910961,
#             " With": 0.022403961047530174,
#             " There": 0.0187936220318079
#         }
#     },
#     "1": {
#         "top_logits": {
#             " aqu": 0.44693803787231445,
#             " New": 0.4136415421962738,
#             " Aqu": 0.10201377421617508,
#             " Boston": 0.006641479209065437,
#             " largest": 0.00443438021466136,
#             " place": 0.0017467315774410963,
#             " facility": 0.0014324766816571355,
#             " large": 0.0012487838976085186
#         }
#     },
#     "2": {
#         "top_logits": {
#             "arium": 0.9999651908874512,
#             "ari": 1.4034872947377153e-05,
#             "aram": 5.639155006065266e-06,
#             "a": 2.876637836379814e-06,
#             "ar": 2.706826307985466e-06,
#             "rium": 2.4531620965717593e-06,
#             "aria": 1.6149072052940028e-06,
#             "arius": 1.2960473441125941e-06
#         }
#     },
#     "3": {
#         "top_logits": {
#             " is": 0.8619698882102966,
#             " has": 0.05918322131037712,
#             " features": 0.018216397613286972,
#             " offers": 0.01645832136273384,
#             " was": 0.014184875413775444,
#             " houses": 0.005421501584351063,
#             " opened": 0.004394961055368185,
#             ",": 0.003026373451575637
#         }
#     },
#     "4": {
#         "top_logits": {
#             " located": 0.4782085716724396,
#             " home": 0.27878686785697937,
#             " a": 0.09264256060123444,
#             " one": 0.05401458963751793,
#             " situated": 0.017215535044670105,
#             " an": 0.014790067449212074,
#             " dedicated": 0.007082248106598854,
#             " known": 0.0053869145922362804
#         }
#     },
#     "5": {
#         "top_logits": {
#             " world": 0.16462449729442596,
#             " global": 0.12381993979215622,
#             " must": 0.09584621340036392,
#             " non": 0.08767339587211609,
#             " large": 0.07530642300844193,
#             " popular": 0.06255023181438446,
#             " major": 0.04755894094705582,
#             " wonderful": 0.04009266942739487
#         }
#     },
 