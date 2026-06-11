#!/usr/bin/env fish

# Vytvori read-only RPC request pre Worker a ulozi ho do inboxu.

function log_info -a message
    echo "🧠 $message"
end

function log_done -a message
    echo "✅ $message"
end

function log_error -a message
    echo "❌ $message" >&2
end

function find_project_python
    # Preferujeme projektovy virtualenv, aby bol import modulu stabilny.
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
set -l FILE_PATH ""
set -l MAX_BYTES ""

if set -q _flag_path
    set FILE_PATH $_flag_path
end
if set -q _flag_max_bytes
    set MAX_BYTES $_flag_max_bytes
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
set -l COMMAND $PYTHON_CMD -m primesymbolicmdl.ap_rpc request --repo-root $REPO_ROOT --method $METHOD
if test -n "$FILE_PATH"
    set COMMAND $COMMAND --path $FILE_PATH
end
if test -n "$MAX_BYTES"
    set COMMAND $COMMAND --max-bytes $MAX_BYTES
end

log_info "Vytvaram RPC request pre metodu $METHOD ..."
set -l META_JSON ($COMMAND 2>&1)
set -l EXIT_CODE $status
if test $EXIT_CODE -ne 0
    log_error "RPC request creation failed."
    printf "%s\n" "$META_JSON" >&2
    exit $EXIT_CODE
end

set -l REQUEST_ID (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["request_id"])')
set -l REQUEST_PATH (printf "%s\n" "$META_JSON" | $PYTHON_CMD -c 'import json,sys; print(json.load(sys.stdin)["request_path"])')

log_done "RPC request ulozeny do $REQUEST_PATH"
echo "REQUEST_ID=$REQUEST_ID"
echo "REQUEST_PATH=$REQUEST_PATH"
