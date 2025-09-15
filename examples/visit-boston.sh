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
    -vv \
    encode \
    --text "hey"

# A great place to visit in boston is the New England Aquarium. The Aquarium is a world leader in ocean exploration and marine conservation research. They have over a thousand animals and a wide