#!/usr/bin/env fish

# Uzatvara jeden Worker cyklus: testy, snapshot, chat zaznam a kratky stav.

function log_info -a message
    echo "🧠 $message"
end

function log_warn -a message
    echo "⚠️  $message"
end

function log_done -a message
    echo "✅ $message"
end

function find_project_python
    # Najprv skusime bezne virtualenv cesty v repozitari.
    for candidate in "$PWD/.venv/bin/python" "$PWD/venv/bin/python"
        if test -x $candidate
            echo $candidate
            return 0
        end
    end

    # Fallback: najdeme hocijaky lokalny python pod repozitarom.
    set -l discovered (find . -maxdepth 4 -path '*/bin/python' 2>/dev/null | head -n 1)
    if test -n "$discovered"
        echo $discovered
        return 0
    end

    return 1
end

function collect_changed_files
    # Poskladame modifikovane aj untracked subory a odfiltrujeme generated handoff artefakty.
    begin
        git diff --name-only -- . ':!BRAIN.md' ':!BOOT.md' ':!NEXT_AGENT.md' ':!NEXT_AGENT_*.md'
        git ls-files --others --exclude-standard
    end | sed '/^BRAIN\.md$/d;/^BOOT\.md$/d;/^NEXT_AGENT\(_[0-9]\+\)\?\.md$/d;/^\.ap\//d' | sort -u
end

argparse 'message=' 'tldr=' -- $argv
or begin
    echo "❌ Invalid arguments."
    exit 2
end

if not set -q _flag_message
    echo "❌ --message is required."
    exit 2
end

set -l MESSAGE $_flag_message
set -l TLDR $_flag_tldr
if test -z "$TLDR"
    set TLDR "$MESSAGE"
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT

set -l TMP_DIR (mktemp -d)
set -l TIMESTAMP (date -Iseconds)
set -l TEST_OUTPUT_FILE "$TMP_DIR/test_output.txt"
set -l SNAPSHOT_OUTPUT_FILE "$TMP_DIR/snapshot_output.txt"
set -l CHAT_OUTPUT_FILE "$TMP_DIR/chat_output.txt"
set -l AP_DIR ".ap"
set -l CURRENT_STATUS_FILE "$AP_DIR/current_status.md"
set -l LAST_REPORT_FILE "$AP_DIR/last_report.md"

mkdir -p $AP_DIR

set -l TEST_STATUS "failed"
set -l TEST_RUNNER "python -m pytest -q"
set -l SNAPSHOT_STATUS "not run"
set -l CHAT_STATUS "not appended"
set -l FINAL_EXIT 0

log_info "Running worker cycle tests ..."
python -m pytest -q > $TEST_OUTPUT_FILE 2>&1
set -l TEST_EXIT $status
if test $TEST_EXIT -eq 0
    set TEST_STATUS "passed"
else
    set -l PROJECT_PYTHON (find_project_python)
    if test -n "$PROJECT_PYTHON"; and string match -rq 'No module named pytest' -- (string join \n -- (cat $TEST_OUTPUT_FILE))
        log_warn "System python has no pytest, retrying with project virtual environment python."
        $PROJECT_PYTHON -m pytest -q > $TEST_OUTPUT_FILE 2>&1
        set TEST_EXIT $status
        set TEST_RUNNER "project virtual environment python -m pytest -q"
    end

    if test $TEST_EXIT -eq 0
        set TEST_STATUS "passed"
    else
        set TEST_STATUS "failed"
        set FINAL_EXIT 1
    end
end

log_info "Refreshing repository snapshot ..."
fish scripts/ap_snapshot.fish --run-tests > $SNAPSHOT_OUTPUT_FILE 2>&1
set -l SNAPSHOT_EXIT $status
if test $SNAPSHOT_EXIT -eq 0
    set SNAPSHOT_STATUS "generated"
else
    set SNAPSHOT_STATUS "failed"
    log_warn "Snapshot regeneration failed."
    if test $FINAL_EXIT -eq 0
        set FINAL_EXIT 1
    end
end

set -l STATUS_NOTE "Cycle close result: tests passed and snapshot refreshed."
if test "$TEST_STATUS" = "failed"
    set STATUS_NOTE "Cycle close result: tests failed."
else if test "$SNAPSHOT_STATUS" != "generated"
    set STATUS_NOTE "Cycle close result: tests passed but snapshot regeneration failed."
end

set -l CHAT_MESSAGE "$MESSAGE Status note: $STATUS_NOTE"
set -l CHAT_TLDR "$TLDR | Test status: $TEST_STATUS | Snapshot status: $SNAPSHOT_STATUS"
set -l COMMANDS_TEXT "python -m pytest -q; fish scripts/ap_snapshot.fish --run-tests"
set -l FILES_TEXT (string join \n (collect_changed_files))

log_info "Appending Worker cycle entry to CHAT.md ..."
fish scripts/ap_chat_append.fish --role worker --message "$CHAT_MESSAGE" --tldr "$CHAT_TLDR" --commands "$COMMANDS_TEXT" --files "$FILES_TEXT" > $CHAT_OUTPUT_FILE 2>&1
set -l CHAT_EXIT $status
if test $CHAT_EXIT -eq 0
    set CHAT_STATUS "appended"
else
    set CHAT_STATUS "failed"
    log_warn "CHAT.md append failed."
    if test $FINAL_EXIT -eq 0
        set FINAL_EXIT 1
    end
end

set -l NEXT_STEP "Review BRAIN.md and choose the next bounded AP task."
if test "$TEST_STATUS" = "failed"
    set NEXT_STEP "Investigate the failing test output before making new code changes."
else if test "$SNAPSHOT_STATUS" != "generated"
    set NEXT_STEP "Fix snapshot regeneration before trusting the AP handoff chain."
end

log_info "Writing $CURRENT_STATUS_FILE ..."
begin
    echo "# Current AP Worker Status"
    echo
    echo "- Generated: `$TIMESTAMP`"
    echo "- Message: `$MESSAGE`"
    echo "- TLDR: `$TLDR`"
    echo "- Test status: `$TEST_STATUS`"
    echo "- Test runner: `$TEST_RUNNER`"
    echo "- Snapshot status: `$SNAPSHOT_STATUS`"
    echo "- CHAT status: `$CHAT_STATUS`"
    echo "- Detail artifacts: `BRAIN.md`, `BOOT.md`, `CHAT.md`, `.ap/last_report.md`"
end > $CURRENT_STATUS_FILE

log_info "Writing $LAST_REPORT_FILE ..."
begin
    echo "### Report for ORCHESTRATOR_CHAT"
    echo
    echo "1. Changed files"
    echo
    if test -n "$FILES_TEXT"
        for path in (string split \n -- $FILES_TEXT)
            set -l trimmed (string trim -- $path)
            if test -n "$trimmed"
                echo "- `$trimmed`"
            end
        end
    else
        echo "- No changed files detected outside generated exclusions."
    end
    echo
    echo "2. Summary"
    echo
    echo "$MESSAGE"
    echo
    echo "TLDR: $TLDR"
    echo
    echo "3. Commands run"
    echo
    echo "- `python -m pytest -q`"
    echo "- `fish scripts/ap_snapshot.fish --run-tests`"
    echo "- `fish scripts/ap_chat_append.fish ...`"
    echo
    echo "4. Test output"
    echo
    echo "- Status: `$TEST_STATUS`"
    echo "- Runner: `$TEST_RUNNER`"
    echo
    echo '```text'
    cat $TEST_OUTPUT_FILE
    echo '```'
    echo
    echo "5. Snapshot status, if applicable"
    echo
    echo "- Snapshot status: `$SNAPSHOT_STATUS`"
    echo "- CHAT status: `$CHAT_STATUS`"
    echo
    echo '```text'
    if test -s $SNAPSHOT_OUTPUT_FILE
        cat $SNAPSHOT_OUTPUT_FILE
    else
        echo "(no snapshot output)"
    end
    echo '```'
    echo
    echo "6. Warnings / limitations"
    echo
    if test "$TEST_STATUS" = "failed"
        echo "- Tests failed during cycle close."
    else
        echo "- Tests passed during cycle close."
    end
    if test "$SNAPSHOT_STATUS" != "generated"
        echo "- Snapshot regeneration failed."
    else
        echo "- Snapshot regeneration completed."
    end
    if test "$CHAT_STATUS" != "appended"
        echo "- CHAT append failed."
    else
        echo "- CHAT entry appended."
    end
    echo
    echo "7. Suggested next smallest step"
    echo
    echo "- $NEXT_STEP"
end > $LAST_REPORT_FILE

log_done "Worker cycle artifacts refreshed."
log_done "Test status: $TEST_STATUS"
log_done "Snapshot status: $SNAPSHOT_STATUS"
log_done "CHAT status: $CHAT_STATUS"

rm -rf $TMP_DIR
exit $FINAL_EXIT
