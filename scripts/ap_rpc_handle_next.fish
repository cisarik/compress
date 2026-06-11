#!/usr/bin/env fish

# Spracuje jeden RPC request z inboxu a zapise response do outboxu.

function log_info -a message
    echo "🧠 $message"
end

function log_done -a message
    echo "✅ $message"
end

function log_warn -a message
    echo "⚠️  $message"
end

function log_error -a message
    echo "❌ $message" >&2
end

function find_project_python
    # Preferujeme projektovy virtualenv, aby handler bezal nad rovnakym Python prostredim.
    for candidate in "$PWD/.venv/bin/python" "$PWD/venv/bin/python"
        if test -x $candidate
            echo $candidate
            return 0
        end
    end

    if command -sq python
        command -s python
        return 0
    end

    return 1
end

argparse 'request=' -- $argv
or begin
    log_error "Invalid arguments."
    exit 2
end

set -l EXPLICIT_REQUEST ""
if set -q _flag_request
    set EXPLICIT_REQUEST $_flag_request
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT

set -l PYTHON_CMD (find_project_python)
if test -z "$PYTHON_CMD"
    log_error "Python was not found."
    exit 1
end

set -lx PYTHONPATH "$REPO_ROOT/src"
set -l COMMAND $PYTHON_CMD -m primesymbolicmdl.ap_rpc handle --repo-root $REPO_ROOT
if test -n "$EXPLICIT_REQUEST"
    set COMMAND $COMMAND --request $EXPLICIT_REQUEST
    log_info "Spracuvam explicitny RPC request $EXPLICIT_REQUEST ..."
else
    log_info "Spracuvam najstarsi RPC request z inboxu ..."
end

set -l META_JSON ($COMMAND 2>&1)
set -l EXIT_CODE $status
if test $EXIT_CODE -ne 0
    log_error "RPC handler failed."
    printf "%s\n" "$META_JSON" >&2
    exit $EXIT_CODE
end

set -l REQUEST_ID (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["request_id"])')
set -l REQUEST_PATH (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["request_path"])')
set -l RESPONSE_PATH (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["response_path"])')
set -l RESPONSE_STATUS (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["response_status"])')
set -l ARCHIVE_PATH (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; value=json.load(sys.stdin)["archive_path"]; print("" if value is None else value)')

log_done "RPC response ulozena do $RESPONSE_PATH"
if test -n "$ARCHIVE_PATH"
    log_done "RPC request archivovany do $ARCHIVE_PATH"
else
    log_warn "RPC request sa nepodarilo archivovat."
end

echo "REQUEST_ID=$REQUEST_ID"
echo "REQUEST_PATH=$REQUEST_PATH"
echo "RESPONSE_PATH=$RESPONSE_PATH"
echo "RESPONSE_STATUS=$RESPONSE_STATUS"
if test -n "$ARCHIVE_PATH"
    echo "ARCHIVE_PATH=$ARCHIVE_PATH"
end
