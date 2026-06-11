#!/usr/bin/env fish

# Lokalny smoke workflow: request -> handle -> kratke zhrnutie response.

function log_info -a message
    echo "🧠 $message"
end

function log_done -a message
    echo "✅ $message"
end

function log_error -a message
    echo "❌ $message" >&2
end

argparse 'method=' 'path=' 'max-bytes=' -- $argv
or begin
    log_error "Invalid arguments."
    exit 2
end

if not set -q _flag_method
    log_error "--method is required."
    exit 2
end

set -l METHOD $_flag_method
set -l FORWARD_ARGS --method $METHOD

if set -q _flag_path
    set FORWARD_ARGS $FORWARD_ARGS --path $_flag_path
end
if set -q _flag_max_bytes
    set FORWARD_ARGS $FORWARD_ARGS --max-bytes $_flag_max_bytes
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT
set -l TMP_DIR (mktemp -d)
set -l REQUEST_LOG "$TMP_DIR/request.log"
set -l HANDLE_LOG "$TMP_DIR/handle.log"

log_info "Spustam lokalny RPC call pre $METHOD ..."
fish scripts/ap_rpc_request.fish $FORWARD_ARGS > $REQUEST_LOG 2>&1
set -l REQUEST_EXIT $status
cat $REQUEST_LOG
if test $REQUEST_EXIT -ne 0
    rm -rf $TMP_DIR
    exit $REQUEST_EXIT
end

set -l REQUEST_PATH (cat $REQUEST_LOG | string match -r '^REQUEST_PATH=.*' | string replace 'REQUEST_PATH=' '')
if test -z "$REQUEST_PATH"
    log_error "Nepodarilo sa zistit REQUEST_PATH."
    rm -rf $TMP_DIR
    exit 1
end

fish scripts/ap_rpc_handle_next.fish --request $REQUEST_PATH > $HANDLE_LOG 2>&1
set -l HANDLE_EXIT $status
cat $HANDLE_LOG
if test $HANDLE_EXIT -ne 0
    rm -rf $TMP_DIR
    exit $HANDLE_EXIT
end

set -l RESPONSE_PATH (cat $HANDLE_LOG | string match -r '^RESPONSE_PATH=.*' | string replace 'RESPONSE_PATH=' '')
set -l RESPONSE_STATUS (cat $HANDLE_LOG | string match -r '^RESPONSE_STATUS=.*' | string replace 'RESPONSE_STATUS=' '')

if test -z "$RESPONSE_PATH"
    log_error "Nepodarilo sa zistit RESPONSE_PATH."
    rm -rf $TMP_DIR
    exit 1
end
if test -z "$RESPONSE_STATUS"
    log_error "Nepodarilo sa zistit RESPONSE_STATUS."
    rm -rf $TMP_DIR
    exit 1
end

log_done "RPC call dokonceny so stavom $RESPONSE_STATUS"
echo "RESPONSE_PATH=$RESPONSE_PATH"
echo "RESPONSE_STATUS=$RESPONSE_STATUS"
rm -rf $TMP_DIR
