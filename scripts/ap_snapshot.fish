#!/usr/bin/env fish

# Generuje analyticky snapshot repozitara pre Orchestrator chat.

set -l BRAIN_OUT "BRAIN.md"
set -l BOOT_OUT "BOOT.md"
set -l MAX_FILE_KB 80
set -l RUN_TESTS 0
set -l TOTAL_CONTENT_BUDGET_KB 1024
set -l DIFF_BUDGET_KB 256

function log_info -a message
    echo "🧠 $message"
end

function log_warn -a message
    echo "⚠️  $message"
end

function log_done -a message
    echo "✅ $message"
end

function sanitize_output
    # Cez cat explicitne preposleme stdin, aby sanitizacia fungovala aj vo fish funkcii.
    cat
end

function find_project_python
    # Najprv skus bezne virtualenv cesty v repozitari.
    for candidate in "$PWD/.venv/bin/python" "$PWD/venv/bin/python"
        if test -x $candidate
            echo $candidate
            return 0
        end
    end

    # Fallback: najdi hocijaky spustitelny python pod repozitarom.
    set -l discovered (find . -maxdepth 4 -path '*/bin/python' 2>/dev/null | head -n 1)
    if test -n "$discovered"
        echo $discovered
        return 0
    end

    return 1
end

function extension_language -a path
    switch $path
        case "*.py"
            echo "python"
        case "*.fish"
            echo "fish"
        case "*.md"
            echo "markdown"
        case "*.toml"
            echo "toml"
        case ".gitignore"
            echo "gitignore"
        case "*.json"
            echo "json"
        case "*.yml" "*.yaml"
            echo "yaml"
        case "*.ini" "*.cfg"
            echo "ini"
        case "*.txt"
            echo "text"
        case '*'
            echo "text"
    end
end

function should_skip_file -a path
    if string match -rq '(^|/)(\.git|\.venv|__pycache__|\.pytest_cache|\.mypy_cache|\.ruff_cache)(/|$)' -- $path
        return 0
    end
    if string match -rq '(^|/)(BRAIN|BOOT)\.md$' -- $path
        return 0
    end
    if string match -rq '(^|/)NEXT_AGENT(_[0-9]+)?\.md$' -- $path
        return 0
    end
    if string match -rq '\.(pyc|png|jpg|jpeg|gif|webp|mp4|mov|zip|sqlite|db)$' -- $path
        return 0
    end
    return 1
end

function collect_candidate_files
    set -l roots src tests docs scripts
    set -l items

    for root in $roots
        if test -d $root
            for item in (find $root -type f | sort)
                set items $items (string replace -r '^\.?/' '' -- $item)
            end
        end
    end

    for root_file in AGENTS.md AP.md AP_WORKER.md COORDINATOR_PROTOCOL.md README.md CHAT.md pyproject.toml .gitignore
        if test -f $root_file
            set items $items $root_file
        end
    end

    printf "%s\n" $items | sort -u
end

argparse 'run-tests' 'max-file-kb=' 'brain=' 'boot=' -- $argv
or begin
    echo "❌ Invalid arguments."
    exit 2
end

if set -q _flag_run_tests
    set RUN_TESTS 1
end
if set -q _flag_max_file_kb
    set MAX_FILE_KB $_flag_max_file_kb
end
if set -q _flag_brain
    set BRAIN_OUT $_flag_brain
end
if set -q _flag_boot
    set BOOT_OUT $_flag_boot
end

if not string match -rq '^[0-9]+$' -- $MAX_FILE_KB
    echo "❌ --max-file-kb must be a non-negative integer."
    exit 2
end

set -l REPO_ROOT (git rev-parse --show-toplevel 2>/dev/null)
if test -z "$REPO_ROOT"
    set REPO_ROOT (pwd)
end
cd $REPO_ROOT

set -l TMP_DIR (mktemp -d)
set -l TIMESTAMP (date -Iseconds)
set -l BRANCH (git branch --show-current 2>/dev/null)
if test -z "$BRANCH"
    set BRANCH "n/a"
end
set -l HEAD_HASH (git rev-parse HEAD 2>/dev/null)
if test -z "$HEAD_HASH"
    set HEAD_HASH "n/a"
end
set -l PYTHON_VERSION (python --version 2>&1)
set -l PYTHON_COMMAND_V (command -v python 2>/dev/null)
set -l PYTHON_PATH (which python 2>/dev/null)
if test -z "$PYTHON_PATH"
    set PYTHON_PATH "python not found"
end
if test -z "$PYTHON_COMMAND_V"
    set PYTHON_COMMAND_V "python not found"
end
set -l PYTHON_SYS_EXECUTABLE (python -c 'import sys; print(sys.executable)' 2>&1)
set -l PYTHON_SYS_PREFIX (python -c 'import sys; print(sys.prefix)' 2>&1)
set -l PROJECT_VENV_EXISTS "no"
if test -d ".venv"
    set PROJECT_VENV_EXISTS "yes"
end
set -l PYTHON_INSIDE_PROJECT_VENV "no"
if string match -rq '(^|/)\.venv/' -- $PYTHON_SYS_EXECUTABLE
    set PYTHON_INSIDE_PROJECT_VENV "yes"
end
set -l PYTHON_ENV_WARNING ""
if test "$PROJECT_VENV_EXISTS" = "yes"; and test "$PYTHON_INSIDE_PROJECT_VENV" != "yes"
    set PYTHON_ENV_WARNING "WARNING: .venv exists but active python is not the project virtual environment."
end

set -l GIT_STATUS_FILE "$TMP_DIR/git_status.txt"
set -l DIFF_STAT_FILE "$TMP_DIR/diff_stat.txt"
set -l FULL_DIFF_FILE "$TMP_DIR/full_diff.txt"
set -l TEST_OUTPUT_FILE "$TMP_DIR/test_output.txt"

git status --short | sed '/NEXT_AGENT\(_[0-9]\+\)\?\.md$/d' > $GIT_STATUS_FILE 2>&1
git diff --stat -- . ':!BRAIN.md' ':!BOOT.md' ':!NEXT_AGENT.md' ':!NEXT_AGENT_*.md' > $DIFF_STAT_FILE 2>&1
git diff -- . ':!BRAIN.md' ':!BOOT.md' ':!NEXT_AGENT.md' ':!NEXT_AGENT_*.md' > $FULL_DIFF_FILE 2>&1

set -l TEST_STATUS "not run"
set -l TEST_RUNNER "not run"
echo "Tests were not run. Use --run-tests to execute pytest." > $TEST_OUTPUT_FILE

if test $RUN_TESTS -eq 1
    log_info "Running tests for snapshot..."
    python -m pytest -q > $TEST_OUTPUT_FILE 2>&1
    set -l TEST_EXIT $status
    if test $TEST_EXIT -eq 0
        set TEST_STATUS "passed"
        set TEST_RUNNER "python -m pytest -q"
    else
        set -l PROJECT_PYTHON (find_project_python)
        if test -n "$PROJECT_PYTHON"; and string match -rq 'No module named pytest' -- (string join \n -- (cat $TEST_OUTPUT_FILE))
            log_warn "System python has no pytest, retrying with project virtual environment python."
            $PROJECT_PYTHON -m pytest -q > $TEST_OUTPUT_FILE 2>&1
            set TEST_EXIT $status
            if test $TEST_EXIT -eq 0
                set TEST_STATUS "passed"
                set TEST_RUNNER "project virtual environment python -m pytest -q"
            else
                set TEST_STATUS "failed"
                set TEST_RUNNER "project virtual environment python -m pytest -q"
            end
        else
            set TEST_STATUS "failed"
            set TEST_RUNNER "python -m pytest -q"
        end
    end
end

log_info "Writing $BRAIN_OUT ..."
begin
    echo "# BRAIN.md — Analytic Coding Repository Snapshot"
    echo
    echo "## 2. Timestamp"
    echo
    echo "- Generated: `$TIMESTAMP`"
    echo
    echo "## 3. Repo Root"
    echo
    echo "- Repo root: `$REPO_ROOT`"
    echo
    echo "## 4. Branch"
    echo
    echo "- Branch: `$BRANCH`"
    echo
    echo "## 5. HEAD Commit"
    echo
    echo "- HEAD: `$HEAD_HASH`"
    echo
    echo "## 6. Python Info"
    echo
    echo "- command -v python: `$PYTHON_COMMAND_V`"
    echo "- python --version: `$PYTHON_VERSION`"
    echo "- which python: `$PYTHON_PATH`"
    echo "- sys.executable: `$PYTHON_SYS_EXECUTABLE`"
    echo "- sys.prefix: `$PYTHON_SYS_PREFIX`"
    echo "- .venv exists: `$PROJECT_VENV_EXISTS`"
    echo "- active python inside .venv: `$PYTHON_INSIDE_PROJECT_VENV`"
    if test -n "$PYTHON_ENV_WARNING"
        echo
        echo "> $PYTHON_ENV_WARNING"
    end
    echo
    echo "## 7. Git Status"
    echo
    echo '```text'
    if test -s $GIT_STATUS_FILE
        cat $GIT_STATUS_FILE | sanitize_output
    else
        echo "(clean working tree)"
    end
    echo '```'
    echo
    echo "## 8. Diff Stat"
    echo
    echo '```text'
    if test -s $DIFF_STAT_FILE
        cat $DIFF_STAT_FILE | sanitize_output
    else
        echo "(no diff stat output)"
    end
    echo '```'
    echo
    echo "## 9. Full Diff"
    echo
    echo '```diff'
    set -l FULL_DIFF_LIMIT_BYTES (math "$DIFF_BUDGET_KB * 1024")
    set -l FULL_DIFF_SIZE (stat -c '%s' -- $FULL_DIFF_FILE 2>/dev/null)
    if test -n "$FULL_DIFF_SIZE"; and test $FULL_DIFF_SIZE -gt $FULL_DIFF_LIMIT_BYTES
        head -c $FULL_DIFF_LIMIT_BYTES $FULL_DIFF_FILE | sanitize_output
        echo
        echo "... TRUNCATED: diff exceeded $DIFF_BUDGET_KB KB budget ..."
    else if test -s $FULL_DIFF_FILE
        cat $FULL_DIFF_FILE | sanitize_output
    else
        echo "(no diff output)"
    end
    echo '```'
    echo
    echo "## 10. Test Output"
    echo
    echo "- Test status: `$TEST_STATUS`"
    echo "- Test runner: `$TEST_RUNNER`"
    echo
    echo '```text'
    if test -s $TEST_OUTPUT_FILE
        cat $TEST_OUTPUT_FILE | sanitize_output
    else
        echo "(no test output)"
    end
    echo '```'
    echo
    echo "## 11. Relevant File Tree"
    echo
    for path in (collect_candidate_files)
        if should_skip_file $path
            continue
        end
        set -l size_bytes (stat -c '%s' -- $path 2>/dev/null)
        if test -z "$size_bytes"
            set size_bytes "?"
        end
        echo "- `$path` ($size_bytes bytes)"
    end
    echo
    echo "## 12. Selected File Contents"
    echo
    set -l INCLUDED_BYTES 0
    set -l TOTAL_CONTENT_LIMIT_BYTES (math "$TOTAL_CONTENT_BUDGET_KB * 1024")
    set -l FILE_LIMIT_BYTES (math "$MAX_FILE_KB * 1024")
    for path in (collect_candidate_files)
        if should_skip_file $path
            continue
        end
        if not test -f $path
            continue
        end
        set -l size_bytes (stat -c '%s' -- $path 2>/dev/null)
        if test -z "$size_bytes"
            set size_bytes 0
        end
        echo "## File: `$path`"
        echo
        set -l language (extension_language $path)
        echo "```$language"
        if test $size_bytes -gt $FILE_LIMIT_BYTES
            echo "SKIPPED: file too large"
        else if test (math "$INCLUDED_BYTES + $size_bytes") -gt $TOTAL_CONTENT_LIMIT_BYTES
            echo "SKIPPED: snapshot content budget exceeded"
        else
            cat $path | sanitize_output
            set INCLUDED_BYTES (math "$INCLUDED_BYTES + $size_bytes")
        end
        echo '```'
        echo
    end
end > $BRAIN_OUT

log_info "Writing $BOOT_OUT ..."
begin
    echo "# BOOT.md — Analytic Coding Boot Summary"
    echo
    echo "PrimeSymbolicMDL je experimentalny lossless compression research harness orientovany na honest MDL accounting, anchor/residual vetvy a male deterministicke baseline experimenty."
    echo
    echo "## Current Git State"
    echo
    echo "- Branch: `$BRANCH`"
    echo "- HEAD: `$HEAD_HASH`"
    echo
    echo "## Last Test Status"
    echo
    if test $RUN_TESTS -eq 1
        echo "- Status: `$TEST_STATUS`"
        echo "- Runner: `$TEST_RUNNER`"
    else
        echo "- Tests were not run during this snapshot."
    end
    echo
    echo "## Main Modules"
    echo
    echo "- block packing"
    echo "- prime/index branch"
    echo "- GP-lite law search"
    echo "- SOMA"
    echo "- Image-predictor"
    echo "- residual codec layer"
    echo "- GUI"
    echo
    echo "## Worker Agent Rules"
    echo
    echo "- no git write commands"
    echo "- make small changes"
    echo "- run tests after meaningful changes"
    echo "- after meaningful changes run `fish scripts/ap_snapshot.fish --run-tests`"
    echo "- report begins with `### Report for ORCHESTRATOR_CHAT`"
    echo
    echo "## Detail Source"
    echo
    echo "- Detailed repository state: `BRAIN.md`"
end > $BOOT_OUT

set -l BRAIN_SIZE (stat -c '%s' -- $BRAIN_OUT 2>/dev/null)
set -l BOOT_SIZE (stat -c '%s' -- $BOOT_OUT 2>/dev/null)

log_done "Snapshot complete."
log_done "$BRAIN_OUT size: $BRAIN_SIZE bytes"
log_done "$BOOT_OUT size: $BOOT_SIZE bytes"
if test $RUN_TESTS -eq 1
    log_done "Test status: $TEST_STATUS"
end

rm -rf $TMP_DIR
