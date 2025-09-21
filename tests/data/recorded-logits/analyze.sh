
# run with an argument of the log file:
# ./analyze.sh the-king-1.log

log_file=$1

echo "analyzing log file: $log_file"

echo "total iterations: $(jq 'keys | length' $log_file)"

echo "total tokens: $(jq '[.[] | .top_logits | length] | add' $log_file)   (for all iters)"

echo "top items for first 5 iters: "
jq 'to_entries
    | .[:5]
    | map({token: (.value.top_logits | to_entries | max_by(.value).key),
    score: (.value.top_logits | to_entries | max_by(.value).value)})' $log_file