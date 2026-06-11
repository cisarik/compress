#!/usr/bin/env fish

# Pridava strukturovany zaznam do CHAT.md bez prepisania historie.

function log_info -a message
    echo "🧠 $message"
end

function log_warn -a message
    echo "⚠️  $message"
end

function log_done -a message
    echo "✅ $message"
end

function ensure_chat_file -a chat_path
    # Ak ledger este neexistuje, vytvorime ho s kratkou hlavickou.
    if not test -f $chat_path
        begin
            echo "# CHAT.md — Analytic Programming Coordination Ledger"
            echo
            echo "Append-only coordination log for User, Orchestrator, and Worker."
            echo
        end > $chat_path
        log_info "Created $chat_path"
    end
end

function emit_bullet_lines -a raw_value
    # Text delime po novych riadkoch a prazdne polozky preskocime.
    for line in (string split \n -- $raw_value)
        set -l trimmed (string trim -- $line)
        if test -n "$trimmed"
            echo "- $trimmed"
        end
    end
end

function emit_command_lines -a raw_value
    # Prikazy akceptuju viacriadkovy vstup alebo bodkociarkou oddelene prikazy.
    if string match -q "*\n*" -- $raw_value
        emit_bullet_lines $raw_value
        return 0
    end

    for line in (string split ';' -- $raw_value)
        set -l trimmed (string trim -- $line)
        if test -n "$trimmed"
            echo "- $trimmed"
        end
    end
end

function emit_file_lines -a raw_value
    # Zoznam suborov vieme rozdelit po novych riadkoch alebo medzerach.
    if string match -q "*\n*" -- $raw_value
        emit_bullet_lines $raw_value
        return 0
    end

    for token in (string split ' ' -- $raw_value)
        set -l trimmed (string trim -- $token)
        if test -n "$trimmed"
            echo "- $trimmed"
        end
    end
end

argparse 'role=' 'message=' 'tldr=' 'commands=' 'files=' -- $argv
or begin
    echo "❌ Invalid arguments."
    exit 2
end

if not set -q _flag_role
    echo "❌ --role is required."
    exit 2
end
if not set -q _flag_message
    echo "❌ --message is required."
    exit 2
end

set -l ROLE $_flag_role
set -l MESSAGE $_flag_message
set -l TLDR ""
set -l COMMANDS_TEXT ""
set -l FILES_TEXT ""

if set -q _flag_tldr
    set TLDR $_flag_tldr
end
if set -q _flag_commands
    set COMMANDS_TEXT $_flag_commands
end
if set -q _flag_files
    set FILES_TEXT $_flag_files
end

switch $ROLE
    case user worker orchestrator
    case '*'
        echo "❌ --role must be one of: user, worker, orchestrator."
        exit 2
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT

set -l CHAT_PATH "CHAT.md"
set -l TIMESTAMP (date -Iseconds)

log_info "Appending $ROLE entry to $CHAT_PATH ..."
ensure_chat_file $CHAT_PATH

begin
    echo "## $TIMESTAMP | role=$ROLE"
    echo
    echo "Message:"
    echo "$MESSAGE"
    echo
    if test -n "$TLDR"
        echo "TLDR:"
        emit_bullet_lines $TLDR
        echo
    end
    if test -n "$COMMANDS_TEXT"
        echo "Commands run:"
        emit_command_lines $COMMANDS_TEXT
        echo
    end
    if test -n "$FILES_TEXT"
        echo "Files changed:"
        emit_file_lines $FILES_TEXT
        echo
    end
end >> $CHAT_PATH

log_done "CHAT.md updated."
