import sys
import traceback

from prolog_structures import Rule, RuleBody, Term, Function, Variable, Atom, Number
from final import Interpreter, Not_unifiable

if __name__ == '__main__':

	interpreter = Interpreter()

	def test_final_1_1 ():
		assert ((interpreter.variables_of_term (Function ("f", [Variable ("X"), Variable ("Y"), Atom ("a")]))) ==
			set([Variable ("X"), Variable ("Y")]))

	def test_final_1_2 ():
		assert ((interpreter.variables_of_term (Function ("p", [Variable ("X"), Variable ("Y"), Atom ("a")]))) ==
			set([Variable ("X"), Variable ("Y")]))

	def test_final_1_3 ():
		r = Rule ((Function ("p", [Variable ("X"), Variable ("Y"), Atom ("a")])), RuleBody([]))
		assert ((interpreter.variables_of_clause (r) ==
			set([Variable ("X"), Variable ("Y")])))

	def test_final_1_4 ():
		h = Function ("p", [Variable ("X"), Variable ("Y"), Atom ("a")])
		b = [Function ("q", [Atom ("a"), Atom ("b"), Atom ("a")])]
		r = Rule (h, RuleBody(b))
		assert  (interpreter.variables_of_clause (r) ==
			set([Variable ("X"), Variable ("Y")]))

	def test_final_2_1 ():
		s = { Variable(("Y")): Number(0), Variable("X"): Variable(("Y")) }
		t = Function ("f", [Variable ("X"), Variable ("Y"), Atom ("a")])
		t_= Function ("f", [Variable ("Y"), Number("0"), Atom ("a")])
		assert (interpreter.substitute_in_term (s, t) == t_)

	def test_final_2_2 ():
		s = { Variable(("Y")): Number(0), Variable("X"): Variable(("Y")) }
		t = Function ("p", [Variable ("X"), Variable ("Y"), Atom ("a")])
		t_ = Function ("p", [Variable ("Y"), Number("0"), Atom ("a")])
		assert (interpreter.substitute_in_term (s, t) == t_)

	def test_final_2_3 ():
		s = { Variable(("Y")): Number(0), Variable("X"): Variable(("Y")) }
		r = Rule ((Function ("p", [Variable ("X"), Variable ("Y"), Atom ("a")])), RuleBody([]))
		r_ = Rule ((Function ("p", [Variable ("Y"), Number("0"), Atom ("a")])), RuleBody([]))
		assert (interpreter.substitute_in_clause (s, r) == r_)

	def test_final_2_4 ():
		s = { Variable(("Y")): Number("0"), Variable("X"): Variable(("Y")) }
		p = Function ("p", [Variable("X"), Variable(("Y")), Atom(("a"))])
		q = Function ("q", [Atom(("a")), Atom(("b")), Atom(("a"))])
		p_ = Function ("p", [Variable(("Y")), Number("0"), Atom(("a"))])
		q_ = Function ("q", [Atom(("a")), Atom(("b")), Atom(("a"))])
		r = Rule (p, RuleBody([q]))
		r_ = Rule (p_, RuleBody([q_]))
		assert (interpreter.substitute_in_clause(s, r) == r_)

	# Test on unification
	def test_final_3_1 ():
		t = Variable ("X")
		t_ = Variable ("Y")
		u = {Variable ("Y"): Variable ("X")}
		u_ = {Variable ("X"): Variable ("Y")}
		assert (interpreter.unify (t, t_) == u or interpreter.unify (t, t_) == u_)

	def test_final_3_2 ():
		t = Variable ("Y")
		t_ = Variable ("X")
		u = {Variable ("X"): Variable ("Y")}
		u_ = {Variable ("Y"): Variable ("X")}
		assert (interpreter.unify (t, t_) == u or interpreter.unify (t, t_) == u_)

	def test_final_3_3 ():
		t = Variable ("Y")
		t_ = Variable ("Y")
		assert (interpreter.unify (t, t_) == {})

	def test_final_3_4 ():
		t = Number("0")
		t_ = Number("0")
		assert (interpreter.unify (t, t_) == {})

	def test_final_3_5 ():
		t = Number ("0")
		t_ = Variable ("Y")
		u = {Variable ("Y"): Number("0")}
		assert (interpreter.unify (t, t_) == u)

	def test_final_3_6 ():
		t = Number("0")
		t_ = Number("1")
		try:
			interpreter.unify (t, t_)
			assert False
		except Not_unifiable:
			assert True

	def test_final_3_7 ():
		t = Function ("f", [Number("0")])
		t_ = Function ("g", [Number("1")])
		try:
			interpreter.unify (t, t_)
			assert False
		except Not_unifiable:
			assert True

	def test_final_3_8 ():
		u = {(Variable ("X")): (Variable ("Y"))}
		u_ = {(Variable ("Y")): (Variable ("X"))}
		t = Function ("f", [Variable ("X")])
		t_ = Function ("f", [Variable ("Y")])
		assert (interpreter.unify (t, t_) == u or interpreter.unify (t, t_) == u_)

	def test_final_3_9 ():
		t1 = Function ("f", [Variable ("X"), Variable ("Y"), Variable ("Y")])
		t2 = Function ("f", [Variable ("Y"), Variable ("Z"), Atom ("a")])
		u = { Variable("X"): Atom("a"), Variable("Y"): Atom("a"), Variable("Z"): Atom("a") }
		assert (interpreter.unify (t1, t2) == u)

	def list2str(l):
		return ('(' + (',' + ' ').join(
			list(map(str, l))) + ')')

	# Test on a simple program
	psimple = [Rule(Function ("f", [Atom("a"), Atom("b")]), RuleBody ([]))]

	def test_final_4_1():
		print ("\n\n################################################################")
		print ("###### Testing the non-deterministic abstract interpreter ######")
		print ("################################################################")
		print (f"Program: {list2str(psimple)}")
		g = [Function ("f", [Atom("a"), Atom("b")])]
		print (f"Goal: {list2str(g)}")
		g_ = interpreter.nondet_query (psimple, g)
		assert (g_ == [Function ("f", [Atom("a"), Atom("b")])])
		print (f"Solution: {list2str(g_)}")

	def test_final_4_2():
		g = [Function ("f", [Variable("X"), Atom("b")])]
		print (f"Goal: {list2str(g)}")
		g_ = interpreter.nondet_query (psimple, g)
		assert (g_ == [Function ("f", [Atom("a"), Atom("b")])]);
		print (f"Solution: {list2str(g_)}")

	def test_final_4_3():
		g = [Function ("f", [Variable ("X"), Variable("Y")])]
		print (f"Goal: {list2str(g)}")
		g_ = interpreter.nondet_query (psimple, g)
		assert (g_ == [Function ("f", [Atom("a"), Atom("b")])])
		print (f"Solution: {list2str(g_)}")


	# Test on the House Stark program
	def ancestor (x, y): return Function ("ancestor", [x, y])
	def father (x, y): return Function ("father", [x, y])
	def father_consts (x, y):  return father (Atom (x), Atom (y))
	f1 = Rule (father_consts ("rickard", "ned"), RuleBody([]))
	f2 = Rule (father_consts ("ned", "robb"), RuleBody([]))
	r1 = Rule (ancestor (Variable ("X"), Variable ("Y")), RuleBody([father (Variable ("X"), Variable ("Y"))]))
	r2 = Rule (ancestor (Variable ("X"), Variable ("Y")), \
					RuleBody([father (Variable ("X"), Variable ("Z")), ancestor (Variable ("Z"), Variable ("Y"))]))
	pstark = [f1,f2,r1,r2]

	def test_final_4_4():
		print (f"\nProgram: {list2str(pstark)}")
		g = [ancestor (Atom("rickard"), Atom("ned"))]
		print (f"Goal: {list2str(g)}")
		g_ = interpreter.nondet_query (pstark, g)
		print (f"Solution: {list2str(g_)}")
		assert (g_ == [ancestor (Atom("rickard"), Atom("ned"))])

	def test_final_4_5():
		g = [ancestor (Atom("rickard"), Atom("robb"))]
		print (f"Goal: {list2str(g)}")
		g_ = interpreter.nondet_query (pstark, g)
		print (f"Solution: {list2str(g_)}")
		assert (g_ == [ancestor (Atom("rickard"), Atom("robb"))])

	def test_final_4_6 ():
		g = [ancestor (Variable("X"), Atom("robb"))]
		print (f"Goal: {list2str(g)}")
		g_ = interpreter.nondet_query (pstark, g)
		print (f"Solution: {list2str(g_)}")
		assert (g_ == [ancestor (Atom("ned"), Atom("robb"))] or
		              g_ == [ancestor (Atom("rickard"), Atom("robb"))])

	# Test on the list append program
	nil = Atom("nil")
	def cons (h, t): return Function ("cons", [h, t])
	def append (x, y, z): return Function ("append", [x, y, z])
	c1 = Rule (append (nil, Variable("Q"), Variable("Q")), RuleBody([]))
	c2 = Rule (append ((cons (Variable("H"), Variable("P"))), Variable("Q"), (cons (Variable("H"), Variable("R")))), \
	                RuleBody([append (Variable("P"), Variable("Q"), Variable("R"))]))
	pappend = [c1, c2]

	def test_final_4_7():
		print (f"\nProgram: {list2str(pappend)}")
		g = [append (Variable("X"), Variable("Y"), \
				(cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))]
		print (f"Goal: {list2str(g)}")
		g_ = interpreter.nondet_query (pappend, g)
		print (f"Solution: {list2str(g_)}")
		assert (
		g_ == [append (nil, (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))), \
								(cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] or
		g_ == [append ((cons (Number("1"), nil)), (cons (Number("2"), (cons (Number("3"), nil)))), \
								(cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] or
		g_ == [append ((cons (Number("1"), (cons (Number("2"), nil)))), (cons (Number("3"), nil)), \
		 						(cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] or
		g_ == [append ((cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))), nil, \
								(cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))] )


	# Test on the simple program
	def test_challenge_1():
		print ("\n\n###################################################")
		print ("###### Testing the deterministic interpreter ######")
		print ("###################################################")
		print (f"Program: {list2str(psimple)}")
		# Tests query failure
		g = [Function ("f", [Atom ("a"), Atom ("c")])]
		print (f"Goal: {list2str(g)}")
		assert (interpreter.det_query (psimple, g) == [])
		print ("Solution: Empty solution")

	# Test on the Stark House program
	def test_challenge_2():
		print (f"\nProgram:{list2str(pstark)}")
		# Tests backtracking
		g = [ancestor (Atom("rickard"), Atom("robb"))]
		print (f"Goal: {list2str(g)}")
		g_ = interpreter.det_query (pstark, g)
		assert (len(g_) == 1)
		g_ = g_[0]
		print (f"Solution: {list2str(g_)}")
		assert (g_ == g)


	def test_challenge_3():
		# Tests choice points
		g = [ancestor (Variable("X"), Atom("robb"))]
		print (f"Goal: {list2str(g)}")
		g_ = interpreter.det_query (pstark, g)
		assert (len(g_) == 2)
		g1, g2 = g_[0], g_[1]
		print (f"Solution: {list2str(g1)}")
		print (f"Solution: {list2str(g2)}")
		assert (g1 == [ancestor (Atom("ned"), Atom("robb"))])
		assert (g2 == [ancestor (Atom("rickard"), Atom("robb"))])

	# Test on the list append program
	def test_challenge_4():
		print (f"\nProgram: {list2str(pappend)}")
		# Tests choice points
		g = [append (Variable("X"), (Variable("Y")), (cons (Number("1"), (cons (Number("2"), (cons (Number("3"), nil)))))))]
		print (f"Goal: {list2str(g)}")
		g_ = interpreter.det_query (pappend, g)
		assert (len(g_) == 4)
		for sg in g_:
			print (f"Solution: {list2str(sg)}")

	error_count = 0

	try:
		test_final_1_1()
		test_final_1_2()
		test_final_1_3()
		test_final_1_4()
	except AssertionError as err:
		error_count += 1
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)
	except:
		error_count += 1
		print("Unexpected error:", sys.exc_info()[0])
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)

	try:
		test_final_2_1()
		test_final_2_2()
		test_final_2_3()
		test_final_2_4()
	except AssertionError as err:
		error_count += 1
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)
	except:
		error_count += 1
		print("Unexpected error:", sys.exc_info()[0])
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)

	try:
		test_final_3_1()
		test_final_3_2()
		test_final_3_3()
		test_final_3_4()
		test_final_3_5()
		test_final_3_6()
		test_final_3_7()
		test_final_3_8()
		test_final_3_9()
	except AssertionError as err:
		error_count += 1
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)
	except:
		error_count += 1
		print("Unexpected error:", sys.exc_info()[0])
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)

	try:
		test_final_4_1()
		test_final_4_2()
		test_final_4_3()
		test_final_4_4()
		test_final_4_5()
		test_final_4_6()
		test_final_4_7()
	except AssertionError as err:
		error_count += 1
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)
	except:
		error_count += 1
		print("Unexpected error:", sys.exc_info()[0])
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)

	try:
		test_challenge_1()
		test_challenge_2()
		test_challenge_3()
		test_challenge_4()
	except AssertionError as err:
		error_count += 1
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)
	except:
		error_count += 1
		print("Unexpected error:", sys.exc_info()[0])
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)

	print (f"{error_count} out of 5 programming questions are incorrect.")

# test:
#!/usr/bin/env python3

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
#  helpers
# ---------------------------------------------------------------------------

def file_get(base_url: str, path: str, user: str, password: str):
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    req = urllib.request.Request(url)
    req.add_header(
        "Authorization",
        "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""


def fetch_manifest(url, user, password,
                   manifest_repo, manifest_date):
    """Pull today's manifest. Returns list of entries."""
    path = (f"repository/{manifest_repo}"
            f"/{manifest_date}/manifest-{manifest_date}.json")
    status, body = file_get(url, path, user, password)

    if status == 200:
        data = json.loads(body)
        entries = data.get("entries", [])
        print(f"Manifest fetched: {len(entries)} total entries for {manifest_date}")
        return entries
    elif status == 404:
        print(f"No manifest found for {manifest_date} — empty window")
        return []
    else:
        print(f"ERROR: Nexus returned {status} for manifest fetch", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Window boundary calculation
# ---------------------------------------------------------------------------

def compute_window_bounds(bundle_window: str, prev_window: str,
                          prev_day_offset: int):
    """
    Returns (window_start, window_end) as UTC datetimes.

    bundle_window and prev_window are 4-digit strings: "0500", "0900", "1300"
    prev_day_offset is 0 (same day) or -1 (previous day).
    """
    today = datetime.now(timezone.utc).date()

    ph = int(prev_window[:2])
    pm = int(prev_window[2:])
    prev_date = today + timedelta(days=prev_day_offset)
    window_start = datetime(prev_date.year, prev_date.month, prev_date.day,
                            ph, pm, 0, tzinfo=timezone.utc)

    ch = int(bundle_window[:2])
    window_end = datetime(today.year, today.month, today.day,
                          ch, 0, 0, tzinfo=timezone.utc)

    return window_start, window_end


def parse_time(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# Manifest filtering
# ---------------------------------------------------------------------------

def filter_to_window(entries, window_start, window_end):
    """
    Return entries whose publishTime falls within [window_start, window_end).
    Sorted ascending by publishTime.

    Deduplication key: (pipeline_id, commit_sha, publish_version)
      - All three match → true duplicate, skip
      - Same pipeline_id + commit_sha but different publish_version → keep both
        (e.g. docker-amd64 and docker-arm64 from the same pipeline)
      - Different pipeline_id → always keep (separate build events)

    entry_map: latest entry per repo_name for YAML trigger generation.
    When a repo publishes multiple distinct versions, all entries are retained
    in the full filtered list but only the latest drives the trigger job.
    """
    in_window = [
        e for e in entries
        if window_start <= parse_time(e["publish_time"]) < window_end
    ]
    in_window.sort(key=lambda e: e["publish_time"])

    # Remove true duplicates using the three-part key
    seen_keys = set()
    deduplicated = []
    for e in in_window:
        key = (
            e.get("pipeline_id", ""),
            e.get("commit_sha", ""),
            e.get("publish_version", ""),
        )
        if key not in seen_keys:
            seen_keys.add(key)
            deduplicated.append(e)

    # entry_map: latest entry per repo_name drives the trigger job
    # (sorted asc → last write = latest publish)
    entry_map = {}
    for e in deduplicated:
        entry_map[e["repo_name"]] = e

    print(f"Entries in window: {len(in_window)} raw, "
          f"{len(deduplicated)} after dedup, "
          f"{len(entry_map)} unique repos")
    return entry_map


# ---------------------------------------------------------------------------
# Layer loading
# ---------------------------------------------------------------------------

def load_layers(layers_file: str):
    """Load and validate layers.yml. Returns list of layer dicts sorted by order."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML not installed. Run: pip3 install pyyaml", file=sys.stderr)
        sys.exit(1)

    path = Path(layers_file)
    if not path.exists():
        print(f"ERROR: layers file not found: {layers_file}", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        config = yaml.safe_load(f)

    layers = sorted(config.get("layers", []), key=lambda l: l["order"])
    print(f"Layers loaded from {layers_file}: {len(layers)} layer(s)")
    for layer in layers:
        repos = layer.get("repos", [])
        print(f"  [{layer['order']}] {layer['name']} — {len(repos)} repo(s)")
    return layers, config.get("intra_layer_threshold_seconds", 120)


# ---------------------------------------------------------------------------
# Intra-layer clustering
# ---------------------------------------------------------------------------

def cluster(entries: list, threshold_s: int) -> list:
    """
    Greedy single-pass clustering by publishTime gap.
    Gap is measured from the LAST entry in the current cluster (not the first).
    Returns list of clusters, each cluster is a list of entries.
    """
    if not entries:
        return []

    clusters = []
    current = [entries[0]]

    for entry in entries[1:]:
        gap = (parse_time(entry["publish_time"])
               - parse_time(current[-1]["publish_time"])).total_seconds()
        if gap <= threshold_s:
            current.append(entry)   # within threshold → parallel
        else:
            clusters.append(current)
            current = [entry]       # gap exceeded → new sub-stage

    clusters.append(current)
    return clusters


# ---------------------------------------------------------------------------
# YAML generation
# ---------------------------------------------------------------------------

def build_yaml(all_stages: list, all_jobs: dict,
               bundle_window: str, manifest_date: str) -> str:
    """
    Serialise the stage list and job dict to a GitLab CI YAML string.
    Written manually to allow inline comments per job.
    """
    lines = [
        f"# Orchestration YAML — window {bundle_window} — {manifest_date}",
        f"# Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"# Stages: {len(all_stages)}  Jobs: {len(all_jobs)}",
        "",
        "variables:",
        '  NEXUS_URL:      "$NEXUS_URL"',
        '  NEXUS_USER:     "$NEXUS_USER"',
        '  NEXUS_PASSWORD: "$NEXUS_PASSWORD"',
        "",
        "stages:",
    ]

    for stage in all_stages:
        lines.append(f"  - {stage}")
    lines.append("")

    for job_name, job in all_jobs.items():
        meta = job.get("_meta", {})
        lines += [
            f"# layer: {meta.get('layer')}  "
            f"sub: {meta.get('sub_stage')}  "
            f"type: {meta.get('build_type')}  "
            f"version: {meta.get('publish_version')}  "
            f"published: {meta.get('publish_time')}",
            f"{job_name}:",
            f"  stage: {job['stage']}",
            f"  trigger:",
            f"    project: \"{job['trigger']['project']}\"",
            f"    branch:  \"{job['trigger']['branch']}\"",
            f"    strategy: depend",
            f"  variables:",
            f'    NEXUS_URL:      "${{NEXUS_URL}}"',
            f'    NEXUS_USER:     "${{NEXUS_USER}}"',
            f'    NEXUS_PASSWORD: "${{NEXUS_PASSWORD}}"',
            f"  rules:",
            f"    - when: always",
            "",
        ]

    # Empty window guard — GitLab requires at least one job
    if not all_jobs:
        lines += [
            "no-op:",
            "  stage: no-op",
            "  tags: [shell]",
            "  script:",
            "    - echo 'No repos published in this window'",
            "  rules:",
            "    - when: always",
        ]
        # Replace stages list with just no-op
        lines = [l for l in lines if not l.startswith("  - ")]
        no_op_idx = next(i for i, l in enumerate(lines) if l == "stages:")
        lines.insert(no_op_idx + 1, "  - no-op")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle-window",       required=True)
    ap.add_argument("--prev-window",         required=True)
    ap.add_argument("--prev-day-offset",     required=True, type=int)
    ap.add_argument("--nexus-url",           required=True)
    ap.add_argument("--nexus-user",          required=True)
    ap.add_argument("--nexus-password",      required=True)
    ap.add_argument("--nexus-manifest-repo", required=True)
    ap.add_argument("--layers-file",         default="layers.yml")
    ap.add_argument("--gitlab-group",        default="")
    ap.add_argument("--default-branch",      default="main")
    ap.add_argument("--threshold",           default=120, type=int)
    ap.add_argument("--output-dir",          default="windows")
    args = ap.parse_args()

    manifest_date = datetime.now(timezone.utc).strftime("%Y%m%d")
    window_label  = f"{args.bundle_window}-{manifest_date}"
    output_dir    = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Orchestration generate — window {args.bundle_window}")
    print(f"  Date      : {manifest_date}")
    print(f"  Threshold : {args.threshold}s")
    print(f"{'='*60}\n")

    # 1. Window bounds
    window_start, window_end = compute_window_bounds(
        args.bundle_window, args.prev_window, args.prev_day_offset
    )
    print(f"Window: {window_start.isoformat()} -> {window_end.isoformat()}\n")

    # 2. Fetch manifest
    all_entries = fetch_manifest(
        args.nexus_url, args.nexus_user, args.nexus_password,
        args.nexus_manifest_repo, manifest_date
    )

    # 3. Filter to window
    entry_map = filter_to_window(all_entries, window_start, window_end)

    # 4. Load layers
    layers, file_threshold = load_layers(args.layers_file)
    threshold = args.threshold if args.threshold != 120 else file_threshold

    # 5. Build stages and jobs
    all_stages      = []
    all_jobs        = {}
    layer_summaries = []

    for layer in layers:
        layer_name  = layer["name"]
        layer_order = layer["order"]
        layer_repos = layer.get("repos", [])

        matched = []
        skipped = []
        for repo_def in layer_repos:
            rname = repo_def["name"]
            if rname in entry_map:
                matched.append((repo_def, entry_map[rname]))
            else:
                skipped.append(rname)

        if not matched:
            print(f"\n  Layer '{layer_name}' (order {layer_order}): "
                  f"no repos in window — skipped")
            layer_summaries.append({
                "layer": layer_name, "order": layer_order,
                "status": "skipped", "sub_stages": [],
                "skipped_repos": skipped,
            })
            continue

        # Sort matched by publishTime for clustering
        matched.sort(key=lambda x: x[1]["publish_time"])
        entries_only = [e for _, e in matched]
        repo_def_map = {e["repo_name"]: rd for rd, e in matched}
        sub_clusters = cluster(entries_only, threshold)

        print(f"\n  Layer '{layer_name}' (order {layer_order}): "
              f"{len(matched)} matched, {len(skipped)} skipped, "
              f"{len(sub_clusters)} sub-stage(s)")

        sub_stage_summaries = []
        for sub_idx, sub_entries in enumerate(sub_clusters):
            parallel   = len(sub_entries) > 1
            mode       = "parallel" if parallel else "sequential"
            stage_name = (f"layer-{layer_order:02d}-{layer_name}"
                          f"-sub{sub_idx:02d}-{mode}")
            all_stages.append(stage_name)

            repos_in_sub = []
            for entry in sub_entries:
                rname    = entry["repo_name"]
                repo_def = repo_def_map[rname]
                safe     = rname.lower().replace("_", "-").replace(" ", "-")
                proj     = repo_def.get(
                    "project_path",
                    f"{args.gitlab_group}/{rname}"
                )
                branch   = entry.get("reference_branch", args.default_branch)

                job_name = f"trigger-{safe}"
                if job_name in all_jobs:
                    job_name = f"trigger-{safe}-l{layer_order:02d}s{sub_idx:02d}"

                all_jobs[job_name] = {
                    "stage":   stage_name,
                    "trigger": {
                        "project":  proj,
                        "branch":   branch,
                        "strategy": "depend",
                    },
                    "variables": {
                        "NEXUS_URL":      "$NEXUS_URL",
                        "NEXUS_USER":     "$NEXUS_USER",
                        "NEXUS_PASSWORD": "$NEXUS_PASSWORD",
                    },
                    "rules": [{"when": "always"}],
                    "_meta": {
                        "layer":           layer_name,
                        "sub_stage":       sub_idx,
                        "build_type":      entry["build_type"],
                        "publish_version": entry["publish_version"],
                        "publish_time":    entry["publish_time"],
                    },
                }
                repos_in_sub.append(rname)
                print(f"    sub{sub_idx:02d} [{mode:10}] "
                      f"{rname:40} {entry['publish_version']}")

            sub_stage_summaries.append({
                "sub_stage": sub_idx, "mode": mode, "repos": repos_in_sub,
            })

        layer_summaries.append({
            "layer":         layer_name,
            "order":         layer_order,
            "status":        "included",
            "sub_stages":    sub_stage_summaries,
            "skipped_repos": skipped,
        })

    # 6. Write YAML
    yaml_content = build_yaml(
        all_stages, all_jobs, args.bundle_window, manifest_date
    )
    yaml_path = output_dir / f"orchestration-{window_label}.yml"
    yaml_path.write_text(yaml_content)

    # 7. Write metadata JSON
    meta = {
        "window":                        args.bundle_window,
        "date":                          manifest_date,
        "window_start":                  window_start.isoformat(),
        "window_end":                    window_end.isoformat(),
        "intra_layer_threshold_seconds": threshold,
        "total_stages":                  len(all_stages),
        "total_jobs":                    len(all_jobs),
        "layers":                        layer_summaries,
    }
    meta_path = output_dir / f"orchestration-{window_label}-metadata.json"
    meta_path.write_text(json.dumps(meta, indent=2))

    # 8. Write dotenv for downstream pipeline stages
    Path("orchestration.env").write_text(
        f"WINDOW_LABEL={window_label}\n"
        f"TOTAL_JOBS={len(all_jobs)}\n"
        f"TOTAL_STAGES={len(all_stages)}\n"
        f"MANIFEST_DATE={manifest_date}\n"
    )

    print(f"\n{'='*60}")
    print(f"  Output : {yaml_path}")
    print(f"  Stages : {len(all_stages)}")
    print(f"  Jobs   : {len(all_jobs)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
