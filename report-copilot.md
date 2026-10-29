# drcode-bench report

Generated: 2026-10-29T04:46:10+00:00  
Runs dir: `runs` · runs: 560 · pairs: 56

## Summary (scenario × combo)

Medians over the repeats of each pair; a single run is a repeat count of 1. The run count links to the artifacts of the pair's median-wall run.

| scenario | combo | runs | verdicts | pass rate | cost $ (med) | score (α·t+β$) | wall-time (median, s) | testing rounds (med) | bug round-trips (med) | sim interventions (med) | output tokens (med) | model requests (med) | tokens by role (med, prompt/compl.) | gate | stability |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s1_happy | deepseek-v4-baseline | [10](20261028-233755-s1_happy-deepseek-v4-baseline-rep0/) | green | 100% | $0.01969 ($0.0177–$0.02269) | 1.8 (1.6–2) | 42 (36–237) | 1 | 0 | 0 | 1 105 (856–1 569) | 9 | x5-airun-large-thinking: 29 968/1 105 | ok | clean |
| s1_happy | ◉ glm-5.3-baseline | [10](20261028-233701-s1_happy-glm-5.3-baseline-rep0/) | green | 100% | $0.01444 ($0.01255–$0.02327) | 1.3 (1.1–2.1) | 12 (9–15) | 1 | 0 | 0 | 560 (434–819) | 9 | x5-airun-code-large: 28 737/560 | ok | clean |
| s1_happy | incredible-four | [10](20261028-234109-s1_happy-incredible-four-rep0/) | green | 100% | $0.02416 ($0.01398–$0.03223) | 2.2 (1.3–2.9) | 113 (36–912) | 1 | 0 | 0 | 2 266 (1 268–2 898) | 11 | x5-airun-code-large: 11 031/167; x5-airun-medium-thinking: 43 038/2 094 | ok | net-retry, net-retry×5 |
| s1_happy | ◉ regular-three | [10](20261028-235902-s1_happy-regular-three-rep0/) | green | 100% | $0.01244 ($0.01117–$0.0175) | 1.1 (1–1.6) | 12 (10–15) | 1 | 0 | 0 | 563 (460–787) | 10 | x5-airun-code-large: 11 050/176; x5-airun-medium: 19 127/376 | ok | clean |
| s2a_bug_followup | deepseek-v4-baseline | [10](20261029-000301-s2a_bug_followup-deepseek-v4-baseline-rep0/) | failed, green | 90% | $0.07958 ($0.05258–$0.1031) | 1.9 (1.7–2.4) | 180 (114–221) | 3 | 2 | 1 | 6 380 (4 402–7 698) | 30 | x5-airun-large-thinking: 108 294/6 380 | ok | stuck-clarif |
| s2a_bug_followup | ◉ glm-5.3-baseline | [10](20261029-000026-s2a_bug_followup-glm-5.3-baseline-rep0/) | green | 100% | $0.05288 ($0.04616–$0.05596) | 1.2 (1.1–1.3) | 42 (33–49) | 3 | 2 | 1 | 2 970 (2 595–3 540) | 28.5 | x5-airun-code-large: 95 399/2 970 | ok | clean |
| s2a_bug_followup | incredible-four | [10](20261029-001228-s2a_bug_followup-incredible-four-rep0/) | green | 100% | $0.08387 ($0.06974–$0.1216) | 2 (1.6–2.9) | 83 (71–133) | 3 | 2 | 1 | 10 687 (8 282–18 570) | 32.5 | x5-airun-code-large: 38 430/1 337; x5-airun-medium-thinking: 137 242/9 316 | ok | clean |
| s2a_bug_followup | regular-three | [10](20261029-001811-s2a_bug_followup-regular-three-rep0/) | failed, green | 90% | $0.04908 ($0.03048–$0.05393) | 1.2 (1–1.3) | 44 (28–51) | 3 | 2 | 1 | 3 554 (2 590–3 962) | 31 | x5-airun-code-large: 37 684/1 240; x5-airun-medium: 65 713/2 281 | ok | stuck-clarif |
| s2b_bug_report | deepseek-v4-baseline | [10](20261029-002433-s2b_bug_report-deepseek-v4-baseline-rep0/) | green | 100% | $0.08603 ($0.08382–$0.1409) | 1.8 (1.8–3) | 200 (168–384) | 3 | 1 | 0 | 6 389 (5 508–13 800) | 32 | x5-airun-large-thinking: 126 215/6 389 | ok | clean |
| s2b_bug_report | ◉ glm-5.3-baseline | [10](20261029-002111-s2b_bug_report-glm-5.3-baseline-rep0/) | green | 100% | $0.06095 ($0.0559–$0.07495) | 1.3 (1.2–1.6) | 48 (42–60) | 3 | 1 | 0 | 3 177 (2 843–5 142) | 33 | x5-airun-code-large: 114 593/3 177 | ok | clean |
| s2b_bug_report | incredible-four | [10](20261029-003505-s2b_bug_report-incredible-four-rep0/) | green | 100% | $0.09506 ($0.07799–$0.1649) | 2 (1.6–3.5) | 94 (74–136) | 3 | 1 | 0 | 11 141 (9 761–17 691) | 36 | x5-airun-code-large: 46 019/1 535; x5-airun-medium-thinking: 164 600/9 630 | ok | clean |
| s2b_bug_report | ◉ regular-three | [10](20261029-004218-s2b_bug_report-regular-three-rep0/) | green | 100% | $0.05552 ($0.04757–$0.07091) | 1.2 (1–1.5) | 58 (52–70) | 3 | 1 | 0 | 3 697 (3 350–4 103) | 34 | x5-airun-code-large: 46 795/1 595; x5-airun-medium: 76 940/2 194 | ok | clean |
| s3_compaction_coder | deepseek-v4-baseline | [10](20261029-004954-s3_compaction_coder-deepseek-v4-baseline-rep0/) | green | 100% | $0.1374 ($0.1132–$0.1755) | 2.3 (1.9–2.9) | 219 (169–306) | 1 | 0 | 0 | 1 874 (853–2 692) | 40 | x5-airun-large-thinking: 208 265/8 231 | ok | clean |
| s3_compaction_coder | glm-5.3-baseline | [10](20261029-004642-s3_compaction_coder-glm-5.3-baseline-rep0/) | green | 100% | $0.1295 ($0.1074–$0.1693) | 2.1 (1.8–2.8) | 53 (46–62) | 1 | 0 | 0 | 1 414 (539–2 456) | 47.5 | x5-airun-code-large: 253 159/5 262 | ok | clean |
| s3_compaction_coder | incredible-four | [10](20261029-010132-s3_compaction_coder-incredible-four-rep0/) | green | 100% | $0.1142 ($0.08635–$0.1665) | 1.9 (1.4–2.7) | 65 (53–81) | 1 | 0 | 0 | 3 390 (2 113–6 418) | 42.5 | x5-airun-code-large: 172 720/1 517; x5-airun-small-thinking: 10 503/4 884; x5-airun-medium-thinking: 53 909/2 872 | ok | clean |
| s3_compaction_coder | ◉ regular-three | [10](20261029-010710-s3_compaction_coder-regular-three-rep0/) | green | 100% | $0.1037 ($0.06098–$0.1541) | 1.7 (1–2.5) | 47 (32–63) | 1 | 0 | 0 | 1 269 (665–1 947) | 45 | x5-airun-code-large: 178 000/1 860; x5-airun-small: 10 527/1 688; x5-airun-medium: 32 307/638 | ok | clean |
| s4_compaction_tester | ◉ deepseek-v4-baseline | [10](20261029-011528-s4_compaction_tester-deepseek-v4-baseline-rep0/) | green | 100% | $0.2991 ($0.2724–$1.245) | 1.3 (1.1–5.2) | 280 (216–448) | 1 | 1 | 0 | 1 494 (1 233–4 419) | 38 | x5-airun-large-thinking: 492 343/12 290 | ok | clean |
| s4_compaction_tester | ◉ glm-5.3-baseline | [10](20261029-011012-s4_compaction_tester-glm-5.3-baseline-rep0/) | green | 100% | $0.653 ($0.2392–$0.6884) | 2.7 (1–2.9) | 92 (85–115) | 1 | 1 | 0 | 2 200 (938–3 235) | 58.5 | x5-airun-code-large: 1 458 634/7 658 | ok | clean |
| s4_compaction_tester | incredible-four | [10](20261029-013116-s4_compaction_tester-incredible-four-rep0/) | green | 100% | $0.6269 ($0.2796–$0.8569) | 2.6 (1.2–3.6) | 311 (145–1031) | 1 | 1 | 0 | 3 726 (1 931–9 491) | 71 | x5-airun-code-large: 937 790/1 599; x5-airun-medium-thinking: 593 184/18 943; x5-airun-small-thinking: 105 227/11 405 | ok | clean |
| s4_compaction_tester | regular-three | [10](20261029-015736-s4_compaction_tester-regular-three-rep0/) | failed, green | 90% | $0.5707 ($0.2778–$1.081) | 2.4 (1.2–4.5) | 92 (61–192) | 1 | 1 | 0 | 2 778 (1 366–3 660) | 61.5 | x5-airun-code-large: 972 712/1 827; x5-airun-medium: 447 590/2 253; x5-airun-small: 99 402/3 716 | ok | clean |
| s5_clarification | deepseek-v4-baseline | [10](20261029-020535-s5_clarification-deepseek-v4-baseline-rep0/) | failed, green | 90% | $0.03557 ($0.008295–$0.05843) | 1.8 (1.5–2.9) | 63 (13–74) | 1 | 0 | 1 | 2 936 (579–3 539) | 12.5 | x5-airun-large-thinking: 48 624/2 936 | no-testing, ok | stuck-clarif |
| s5_clarification | ◉ glm-5.3-baseline | [10](20261029-020337-s5_clarification-glm-5.3-baseline-rep0/) | green | 100% | $0.02606 ($0.0209–$0.03597) | 1.3 (1–1.8) | 15 (12–28) | 1 | 0 | 1 | 2 115 (1 343–3 027) | 12 | x5-airun-code-large: 41 705/2 115 | ok | clean |
| s5_clarification | incredible-four | [10](20261029-020919-s5_clarification-incredible-four-rep0/) | green | 100% | $0.03831 ($0.02943–$0.07028) | 1.9 (1.4–3.4) | 33 (25–53) | 1 | 0 | 1 | 4 607 (3 764–8 215) | 14 | x5-airun-code-large: 22 603/1 175; x5-airun-medium-thinking: 50 664/3 692 | ok | clean |
| s5_clarification | regular-three | [10](20261029-021129-s5_clarification-regular-three-rep0/) | green | 100% | $0.02626 ($0.0204–$0.04998) | 1.3 (1–2.4) | 19 (15–37) | 1 | 0 | 1 | 2 529 (1 812–4 406) | 14 | x5-airun-code-large: 21 317/1 537; x5-airun-medium: 30 080/1 099 | ok | clean |
| s6_queue_priority | deepseek-v4-baseline | [10](20261029-021507-s6_queue_priority-deepseek-v4-baseline-rep0/) | green | 100% | $0.05316 ($0.04278–$0.0742) | 1.8 (1.5–2.6) | 77 (62–103) | 2 | 1 | 0 | 3 387 (2 473–4 648) | 22 | x5-airun-large-thinking: 78 987/3 387 | ok | clean |
| s6_queue_priority | ◉ glm-5.3-baseline | [10](20261029-021300-s6_queue_priority-glm-5.3-baseline-rep0/) | green | 100% | $0.03862 ($0.03356–$0.04403) | 1.3 (1.2–1.5) | 30 (25–34) | 2 | 1 | 0 | 1 668 (1 560–2 083) | 21.5 | x5-airun-code-large: 75 644/1 668 | ok | clean |
| s6_queue_priority | incredible-four | [10](20261029-021932-s6_queue_priority-incredible-four-rep0/) | green | 100% | $0.06453 ($0.04183–$0.1076) | 2.2 (1.4–3.7) | 58 (42–104) | 2 | 1 | 0 | 7 105 (3 984–12 989) | 25.5 | x5-airun-code-large: 32 625/677; x5-airun-medium-thinking: 121 477/6 473 | ok | clean |
| s6_queue_priority | regular-three | [10](20261029-022347-s6_queue_priority-regular-three-rep0/) | failed, green | 90% | $0.03147 ($0.02887–$0.03485) | 1.1 (1–1.2) | 30 (26–33) | 2 | 1 | 0 | 1 744 (1 665–2 670) | 21 | x5-airun-code-large: 28 367/682; x5-airun-medium: 42 553/1 098 | ok | stuck-clarif |
| s7_fault_injection | deepseek-v4-baseline | [10](20261029-022813-s7_fault_injection-deepseek-v4-baseline-rep0/) | green | 100% | $0.01814 ($0.0148–$0.02243) | 1.8 (1.5–2.2) | 45 (37–54) | 1 | 0 | 0 | 834 (637–1 222) | 9 | x5-airun-large-thinking: 28 789/834 | ok | faults×5, net-retry×3 |
| s7_fault_injection | glm-5.3-baseline | [10](20261029-022619-s7_fault_injection-glm-5.3-baseline-rep0/) | green | 100% | $0.01224 ($0.01138–$0.0182) | 1.2 (1.1–1.8) | 29 (28–31) | 1 | 0 | 0 | 478 (399–747) | 8.5 | x5-airun-code-large: 25 033/478 | ok | faults×5, net-retry×3 |
| s7_fault_injection | incredible-four | [10](20261029-023055-s7_fault_injection-incredible-four-rep0/) | green | 100% | $0.01685 ($0.01424–$0.0213) | 1.7 (1.4–2.1) | 34 (32–40) | 1 | 0 | 0 | 1 606 (1 214–2 568) | 10 | x5-airun-code-large: 11 272/192; x5-airun-medium-thinking: 27 140/1 409 | ok | faults×5, net-retry×3 |
| s7_fault_injection | ◉ regular-three | [10](20261029-023342-s7_fault_injection-regular-three-rep0/) | green | 100% | $0.01218 ($0.01009–$0.01358) | 1.2 (1–1.3) | 29 (27–30) | 1 | 0 | 0 | 504 (437–632) | 9.5 | x5-airun-code-large: 11 261/195; x5-airun-medium: 16 723/311 | ok | faults×5, net-retry×3 |
| s8_fix_loop | deepseek-v4-baseline | [10](20261029-023744-s8_fix_loop-deepseek-v4-baseline-rep0/) | green | 100% | $0.06764 ($0.05152–$0.1195) | 2.3 (1.7–4) | 122 (90–229) | 2 | 0 | 0 | 5 432 (3 939–11 626) | 21 | x5-airun-large-thinking: 89 678/5 432 | ok | clean |
| s8_fix_loop | glm-5.3-baseline | [10](20261029-023536-s8_fix_loop-glm-5.3-baseline-rep0/) | green | 100% | $0.04033 ($0.03377–$0.04448) | 1.4 (1.1–1.5) | 30 (25–40) | 2 | 0 | 0 | 2 580 (2 169–3 106) | 17 | x5-airun-code-large: 70 275/2 580 | ok | clean |
| s8_fix_loop | incredible-four | [10](20261029-024513-s8_fix_loop-incredible-four-rep0/) | failed, green | 90% | $0.06695 ($0.04364–$0.1074) | 2.3 (2–3.6) | 62 (40–108) | 2 | 0 | 0 | 7 637 (3 922–15 169) | 23.5 | x5-airun-code-large: 39 365/1 256; x5-airun-medium-thinking: 96 404/6 445 | ok | clean |
| s8_fix_loop | ◉ regular-three | [10](20261029-024925-s8_fix_loop-regular-three-rep0/) | green | 100% | $0.03334 ($0.02967–$0.06962) | 1.1 (1–2.3) | 26 (24–42) | 2 | 0 | 0 | 2 113 (1 585–3 931) | 18.5 | x5-airun-code-large: 30 219/957; x5-airun-medium: 46 473/1 157 | ok | clean |
| s9_research_count | deepseek-v4-baseline | [10](20261029-025219-s9_research_count-deepseek-v4-baseline-rep0/) | green | 100% | $0.01517 ($0.01167–$0.021) | 1.7 (1.3–2.4) | 16 (11–20) | 0 | 0 | 0 | 693 (463–975) | 5 | x5-airun-large-thinking: 24 299/693 | no-testing, commit-mixed | clean |
| s9_research_count | ◉ glm-5.3-baseline | [10](20261029-025147-s9_research_count-glm-5.3-baseline-rep0/) | green | 100% | $0.01062 ($0.008817–$0.01401) | 1.2 (1–1.6) | 4 (3–7) | 0 | 0 | 0 | 414 (241–495) | 4.5 | x5-airun-code-large: 21 305/414 | no-testing, commit-mixed | clean |
| s9_research_count | incredible-four | [10](20261029-025331-s9_research_count-incredible-four-rep0/) | green | 100% | $0.01252 ($0.01183–$0.01589) | 1.4 (1.3–1.8) | 17 (12–24) | 0 | 0 | 0 | 685 (477–855) | 4 | x5-airun-large-thinking: 19 371/685 | no-testing, commit-mixed | clean |
| s9_research_count | regular-three | [10](20261029-025446-s9_research_count-regular-three-rep0/) | green | 100% | $0.01171 ($0.008988–$0.01399) | 1.3 (1–1.6) | 6 (4–11) | 0 | 0 | 0 | 439 (261–545) | 5 | x5-airun-code-large: 23 719/439 | no-testing, commit-mixed | clean |
| s10_research_facts | deepseek-v4-baseline | [10](20261028-225813-s10_research_facts-deepseek-v4-baseline-rep0/) | green | 100% | $0.02766 ($0.02424–$0.035) | 1.6 (1.4–2) | 56 (45–61) | 0 | 0 | 0 | 2 061 (1 641–2 321) | 6 | x5-airun-large-thinking: 37 509/2 061 | no-testing | clean |
| s10_research_facts | glm-5.3-baseline | [10](20261028-225725-s10_research_facts-glm-5.3-baseline-rep0/) | failed, green | 90% | $0.02082 ($0.01674–$0.02508) | 1.2 (1–1.4) | 10 (8–13) | 0 | 0 | 0 | 1 355 (1 057–1 578) | 7 | x5-airun-code-large: 37 721/1 355 | no-testing | clean |
| s10_research_facts | incredible-four | [10](20261028-230119-s10_research_facts-incredible-four-rep0/) | green | 100% | $0.02608 ($0.02519–$0.02979) | 1.5 (1.4–1.7) | 48 (40–59) | 0 | 0 | 0 | 1 851 (1 583–2 131) | 6 | x5-airun-large-thinking: 37 643/1 851 | no-testing | clean |
| s10_research_facts | ◉ regular-three | [10](20261028-230427-s10_research_facts-regular-three-rep0/) | green | 100% | $0.02125 ($0.01865–$0.02375) | 1.2 (1–1.3) | 10 (9–16) | 0 | 0 | 0 | 1 416 (1 242–1 518) | 7 | x5-airun-code-large: 38 014/1 416 | no-testing | clean |
| s11_research_routes | deepseek-v4-baseline | [10](20261028-230620-s11_research_routes-deepseek-v4-baseline-rep0/) | green | 100% | $0.01928 ($0.01574–$0.02298) | 1.6 (1.3–2) | 22 (18–30) | 0 | 0 | 0 | 798 (667–909) | 6 | x5-airun-large-thinking: 31 646/798 | no-testing | clean |
| s11_research_routes | ◉ glm-5.3-baseline | [10](20261028-230535-s11_research_routes-glm-5.3-baseline-rep0/) | green | 100% | $0.01212 ($0.01175–$0.01449) | 1 (1–1.2) | 6 (5–11) | 0 | 0 | 0 | 419 (343–497) | 5 | x5-airun-code-large: 24 590/419 | no-testing | clean |
| s11_research_routes | incredible-four | [10](20261028-230753-s11_research_routes-incredible-four-rep0/) | green | 100% | $0.01948 ($0.01578–$0.02281) | 1.7 (1.3–1.9) | 25 (17–32) | 0 | 0 | 0 | 805 (663–909) | 6 | x5-airun-large-thinking: 31 795/805 | no-testing | clean |
| s11_research_routes | regular-three | [10](20261028-230936-s11_research_routes-regular-three-rep0/) | green | 100% | $0.01244 ($0.01184–$0.0151) | 1.1 (1–1.3) | 6 (5–13) | 0 | 0 | 0 | 456 (359–543) | 5 | x5-airun-code-large: 25 286/456 | no-testing | clean |
| s12_research_bug_report | deepseek-v4-baseline | [10](20261028-231154-s12_research_bug_report-deepseek-v4-baseline-rep0/) | green | 100% | $0.04201 ($0.03349–$0.04665) | 1.8 (1.4–2) | 80 (64–96) | 1 | 1 | 0 | 2 998 (2 459–3 386) | 14.5 | x5-airun-large-thinking: 59 344/2 998 | ok | clean |
| s12_research_bug_report | glm-5.3-baseline | [10](20261028-231015-s12_research_bug_report-glm-5.3-baseline-rep0/) | failed, green | 90% | $0.02971 ($0.02649–$0.05584) | 1.2 (1.1–2.2) | 22 (16–40) | 1 | 1 | 0 | 1 982 (1 536–3 992) | 13 | x5-airun-code-large: 54 181/1 982 | ok | clean |
| s12_research_bug_report | ◉ incredible-four | [10](20261028-231631-s12_research_bug_report-incredible-four-rep0/) | green | 100% | $0.03999 ($0.03281–$0.05111) | 1.7 (1.4–2.2) | 62 (53–80) | 1 | 1 | 0 | 3 652 (3 220–5 154) | 16 | x5-airun-large-thinking: 24 523/1 601; x5-airun-code-large: 11 269/356; x5-airun-medium-thinking: 36 276/1 845 | ok | clean |
| s12_research_bug_report | regular-three | [10](20261028-232021-s12_research_bug_report-regular-three-rep0/) | failed, green | 90% | $0.02618 ($0.02371–$0.04447) | 1.1 (1–1.4) | 21 (17–34) | 1 | 1 | 0 | 2 006 (1 734–3 956) | 13 | x5-airun-code-large: 26 805/1 263; x5-airun-medium: 26 785/685 | ok | clean |
| s13_research_feature | deepseek-v4-baseline | [10](20261028-232423-s13_research_feature-deepseek-v4-baseline-rep0/) | green | 100% | $0.05885 ($0.04703–$0.06798) | 1.8 (1.4–2.1) | 119 (100–145) | 1 | 0 | 0 | 4 166 (3 657–4 989) | 17 | x5-airun-large-thinking: 83 940/4 166 | ok | clean |
| s13_research_feature | glm-5.3-baseline | [10](20261028-232236-s13_research_feature-glm-5.3-baseline-rep0/) | green | 100% | $0.04127 ($0.03554–$0.06322) | 1.3 (1.1–1.9) | 24 (19–35) | 1 | 0 | 0 | 2 203 (1 983–3 016) | 18.5 | x5-airun-code-large: 77 484/2 203 | ok | clean |
| s13_research_feature | incredible-four | [10](20261028-233104-s13_research_feature-incredible-four-rep0/) | green | 100% | $0.04911 ($0.03785–$0.06404) | 1.5 (1.2–2) | 60 (50–67) | 1 | 0 | 0 | 4 309 (2 988–6 018) | 17.5 | x5-airun-large-thinking: 20 272/1 087; x5-airun-code-large: 23 098/966; x5-airun-medium-thinking: 44 827/1 965 | ok | clean |
| s13_research_feature | ◉ regular-three | [10](20261028-233520-s13_research_feature-regular-three-rep0/) | green | 100% | $0.03959 ($0.03269–$0.04843) | 1.2 (1–1.5) | 22 (20–28) | 1 | 0 | 0 | 2 640 (2 205–3 035) | 17.5 | x5-airun-code-large: 43 951/2 020; x5-airun-medium: 34 637/689 | ok | clean |

## Scenario winners (quality ranking)

Per scenario, the combos ranked lexicographically by (worst verdict, pass rate, cost): green beats settled-but-flagged beats failed/unknown, then the share of green repeats, then ascending cost = α·t_norm + β·m_norm (α = `--time-weight`, default 0 = money only; β fixed at 1). t_norm / m_norm — the pair's median wall-time / cost relative to the scenario's best green repeat (the fastest / cheapest green run → 1.0); unpriced pairs (`—`) rank after priced ones by wall-time.

| scenario | rank | combo | outcome | pass rate | wall-time (med, s) | cost $ (med) | t_norm | m_norm | score |
|---|---|---|---|---|---|---|---|---|---|
| s1_happy | 1 | regular-three | green | 100% | 12.1 | $0.01244 | 1.34 | 1.11 | 1.1 |
| s1_happy | 2 | glm-5.3-baseline | green | 100% | 12 | $0.01444 | 1.33 | 1.29 | 1.3 |
| s1_happy | 3 | deepseek-v4-baseline | green | 100% | 42.2 | $0.01969 | 4.68 | 1.76 | 1.8 |
| s1_happy | 4 | incredible-four | green | 100% | 112.8 | $0.02416 | 12.5 | 2.16 | 2.2 |
| s2a_bug_followup | 1 | glm-5.3-baseline | green | 100% | 41.7 | $0.05288 | 1.26 | 1.24 | 1.2 |
| s2a_bug_followup | 2 | incredible-four | green | 100% | 82.8 | $0.08387 | 2.49 | 1.97 | 2 |
| s2a_bug_followup | 3 | regular-three | failed | 90% | 43.6 | $0.04908 | 1.31 | 1.15 | 1.2 |
| s2a_bug_followup | 4 | deepseek-v4-baseline | failed | 90% | 180.1 | $0.07958 | 5.42 | 1.87 | 1.9 |
| s2b_bug_report | 1 | regular-three | green | 100% | 57.7 | $0.05552 | 1.37 | 1.17 | 1.2 |
| s2b_bug_report | 2 | glm-5.3-baseline | green | 100% | 48.3 | $0.06095 | 1.15 | 1.28 | 1.3 |
| s2b_bug_report | 3 | deepseek-v4-baseline | green | 100% | 199.6 | $0.08603 | 4.74 | 1.81 | 1.8 |
| s2b_bug_report | 4 | incredible-four | green | 100% | 94.3 | $0.09506 | 2.24 | 2 | 2 |
| s3_compaction_coder | 1 | regular-three | green | 100% | 46.6 | $0.1037 | 1.45 | 1.7 | 1.7 |
| s3_compaction_coder | 2 | incredible-four | green | 100% | 65.2 | $0.1142 | 2.03 | 1.87 | 1.9 |
| s3_compaction_coder | 3 | glm-5.3-baseline | green | 100% | 52.7 | $0.1295 | 1.64 | 2.12 | 2.1 |
| s3_compaction_coder | 4 | deepseek-v4-baseline | green | 100% | 219.1 | $0.1374 | 6.83 | 2.25 | 2.3 |
| s4_compaction_tester | 1 | deepseek-v4-baseline | green | 100% | 280.2 | $0.2991 | 4.05 | 1.25 | 1.3 |
| s4_compaction_tester | 2 | incredible-four | green | 100% | 311.4 | $0.6269 | 4.5 | 2.62 | 2.6 |
| s4_compaction_tester | 3 | glm-5.3-baseline | green | 100% | 91.9 | $0.653 | 1.33 | 2.73 | 2.7 |
| s4_compaction_tester | 4 | regular-three | failed | 90% | 92.4 | $0.5707 | 1.34 | 2.39 | 2.4 |
| s5_clarification | 1 | glm-5.3-baseline | green | 100% | 15.2 | $0.02606 | 1.25 | 1.28 | 1.3 |
| s5_clarification | 2 | regular-three | green | 100% | 19.1 | $0.02626 | 1.57 | 1.29 | 1.3 |
| s5_clarification | 3 | incredible-four | green | 100% | 33.2 | $0.03831 | 2.72 | 1.88 | 1.9 |
| s5_clarification | 4 | deepseek-v4-baseline | failed | 90% | 62.8 | $0.03557 | 5.15 | 1.74 | 1.8 |
| s6_queue_priority | 1 | glm-5.3-baseline | green | 100% | 29.6 | $0.03862 | 1.18 | 1.34 | 1.3 |
| s6_queue_priority | 2 | deepseek-v4-baseline | green | 100% | 77.3 | $0.05316 | 3.08 | 1.84 | 1.8 |
| s6_queue_priority | 3 | incredible-four | green | 100% | 57.8 | $0.06453 | 2.31 | 2.24 | 2.2 |
| s6_queue_priority | 4 | regular-three | failed | 90% | 30.2 | $0.03147 | 1.2 | 1.09 | 1.1 |
| s7_fault_injection | 1 | regular-three | green | 100% | 28.6 | $0.01218 | 1.06 | 1.21 | 1.2 |
| s7_fault_injection | 2 | glm-5.3-baseline | green | 100% | 29.2 | $0.01224 | 1.08 | 1.21 | 1.2 |
| s7_fault_injection | 3 | incredible-four | green | 100% | 33.7 | $0.01685 | 1.24 | 1.67 | 1.7 |
| s7_fault_injection | 4 | deepseek-v4-baseline | green | 100% | 45.1 | $0.01814 | 1.67 | 1.8 | 1.8 |
| s8_fix_loop | 1 | regular-three | green | 100% | 26.1 | $0.03334 | 1.08 | 1.12 | 1.1 |
| s8_fix_loop | 2 | glm-5.3-baseline | green | 100% | 30.1 | $0.04033 | 1.25 | 1.36 | 1.4 |
| s8_fix_loop | 3 | deepseek-v4-baseline | green | 100% | 121.9 | $0.06764 | 5.07 | 2.28 | 2.3 |
| s8_fix_loop | 4 | incredible-four | failed | 90% | 61.6 | $0.06695 | 2.56 | 2.26 | 2.3 |
| s9_research_count | 1 | glm-5.3-baseline | green | 100% | 4 | $0.01062 | 1.32 | 1.21 | 1.2 |
| s9_research_count | 2 | regular-three | green | 100% | 5.5 | $0.01171 | 1.82 | 1.33 | 1.3 |
| s9_research_count | 3 | incredible-four | green | 100% | 17.1 | $0.01252 | 5.66 | 1.42 | 1.4 |
| s9_research_count | 4 | deepseek-v4-baseline | green | 100% | 16.1 | $0.01517 | 5.33 | 1.72 | 1.7 |
| s10_research_facts | 1 | regular-three | green | 100% | 10.5 | $0.02125 | 1.3 | 1.2 | 1.2 |
| s10_research_facts | 2 | incredible-four | green | 100% | 47.6 | $0.02608 | 5.91 | 1.47 | 1.5 |
| s10_research_facts | 3 | deepseek-v4-baseline | green | 100% | 56.2 | $0.02766 | 6.97 | 1.56 | 1.6 |
| s10_research_facts | 4 | glm-5.3-baseline | failed | 90% | 9.5 | $0.02082 | 1.18 | 1.17 | 1.2 |
| s11_research_routes | 1 | glm-5.3-baseline | green | 100% | 6 | $0.01212 | 1.2 | 1.03 | 1 |
| s11_research_routes | 2 | regular-three | green | 100% | 6 | $0.01244 | 1.2 | 1.06 | 1.1 |
| s11_research_routes | 3 | deepseek-v4-baseline | green | 100% | 22 | $0.01928 | 4.39 | 1.64 | 1.6 |
| s11_research_routes | 4 | incredible-four | green | 100% | 25.1 | $0.01948 | 5.01 | 1.66 | 1.7 |
| s12_research_bug_report | 1 | incredible-four | green | 100% | 61.7 | $0.03999 | 3.82 | 1.69 | 1.7 |
| s12_research_bug_report | 2 | deepseek-v4-baseline | green | 100% | 80.3 | $0.04201 | 4.97 | 1.77 | 1.8 |
| s12_research_bug_report | 3 | regular-three | failed | 90% | 20.6 | $0.02618 | 1.28 | 1.1 | 1.1 |
| s12_research_bug_report | 4 | glm-5.3-baseline | failed | 90% | 22.1 | $0.02971 | 1.37 | 1.25 | 1.2 |
| s13_research_feature | 1 | regular-three | green | 100% | 22.2 | $0.03959 | 1.16 | 1.21 | 1.2 |
| s13_research_feature | 2 | glm-5.3-baseline | green | 100% | 24.1 | $0.04127 | 1.26 | 1.26 | 1.3 |
| s13_research_feature | 3 | incredible-four | green | 100% | 60.3 | $0.04911 | 3.15 | 1.5 | 1.5 |
| s13_research_feature | 4 | deepseek-v4-baseline | green | 100% | 119.3 | $0.05885 | 6.24 | 1.8 | 1.8 |

## Runs

| run | scenario | combo | verdict | wall-time | report_committed | compactions (ok/started/failed) | testing rounds | sim interventions | tasks | gate | stability | artifacts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [20261028-233755-s1_happy-deepseek-v4-baseline-rep0](20261028-233755-s1_happy-deepseek-v4-baseline-rep0/) | s1_happy | deepseek-v4-baseline | green | 40.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233755-s1_happy-deepseek-v4-baseline-rep0/metrics.json) · [result](20261028-233755-s1_happy-deepseek-v4-baseline-rep0/result.json) |
| [20261028-233812-s1_happy-deepseek-v4-baseline-rep1](20261028-233812-s1_happy-deepseek-v4-baseline-rep1/) | s1_happy | deepseek-v4-baseline | green | 39.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233812-s1_happy-deepseek-v4-baseline-rep1/metrics.json) · [result](20261028-233812-s1_happy-deepseek-v4-baseline-rep1/result.json) |
| [20261028-233816-s1_happy-deepseek-v4-baseline-rep2](20261028-233816-s1_happy-deepseek-v4-baseline-rep2/) | s1_happy | deepseek-v4-baseline | green | 36.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233816-s1_happy-deepseek-v4-baseline-rep2/metrics.json) · [result](20261028-233816-s1_happy-deepseek-v4-baseline-rep2/result.json) |
| [20261028-233841-s1_happy-deepseek-v4-baseline-rep3](20261028-233841-s1_happy-deepseek-v4-baseline-rep3/) | s1_happy | deepseek-v4-baseline | green | 38.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233841-s1_happy-deepseek-v4-baseline-rep3/metrics.json) · [result](20261028-233841-s1_happy-deepseek-v4-baseline-rep3/result.json) |
| [20261028-233857-s1_happy-deepseek-v4-baseline-rep4](20261028-233857-s1_happy-deepseek-v4-baseline-rep4/) | s1_happy | deepseek-v4-baseline | green | 44.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233857-s1_happy-deepseek-v4-baseline-rep4/metrics.json) · [result](20261028-233857-s1_happy-deepseek-v4-baseline-rep4/result.json) |
| [20261028-233858-s1_happy-deepseek-v4-baseline-rep5](20261028-233858-s1_happy-deepseek-v4-baseline-rep5/) | s1_happy | deepseek-v4-baseline | green | 45.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233858-s1_happy-deepseek-v4-baseline-rep5/metrics.json) · [result](20261028-233858-s1_happy-deepseek-v4-baseline-rep5/result.json) |
| [20261028-233931-s1_happy-deepseek-v4-baseline-rep6](20261028-233931-s1_happy-deepseek-v4-baseline-rep6/) | s1_happy | deepseek-v4-baseline | green | 40.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233931-s1_happy-deepseek-v4-baseline-rep6/metrics.json) · [result](20261028-233931-s1_happy-deepseek-v4-baseline-rep6/result.json) |
| [20261028-233948-s1_happy-deepseek-v4-baseline-rep7](20261028-233948-s1_happy-deepseek-v4-baseline-rep7/) | s1_happy | deepseek-v4-baseline | green | 71.3 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233948-s1_happy-deepseek-v4-baseline-rep7/metrics.json) · [result](20261028-233948-s1_happy-deepseek-v4-baseline-rep7/result.json) |
| [20261028-233949-s1_happy-deepseek-v4-baseline-rep8](20261028-233949-s1_happy-deepseek-v4-baseline-rep8/) | s1_happy | deepseek-v4-baseline | green | 76.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233949-s1_happy-deepseek-v4-baseline-rep8/metrics.json) · [result](20261028-233949-s1_happy-deepseek-v4-baseline-rep8/result.json) |
| [20261028-234017-s1_happy-deepseek-v4-baseline-rep9](20261028-234017-s1_happy-deepseek-v4-baseline-rep9/) | s1_happy | deepseek-v4-baseline | green | 236.6 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-234017-s1_happy-deepseek-v4-baseline-rep9/metrics.json) · [result](20261028-234017-s1_happy-deepseek-v4-baseline-rep9/result.json) |
| [20261028-233701-s1_happy-glm-5.3-baseline-rep0](20261028-233701-s1_happy-glm-5.3-baseline-rep0/) | s1_happy | glm-5.3-baseline | green | 12.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233701-s1_happy-glm-5.3-baseline-rep0/metrics.json) · [result](20261028-233701-s1_happy-glm-5.3-baseline-rep0/result.json) |
| [20261028-233704-s1_happy-glm-5.3-baseline-rep1](20261028-233704-s1_happy-glm-5.3-baseline-rep1/) | s1_happy | glm-5.3-baseline | green | 12.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233704-s1_happy-glm-5.3-baseline-rep1/metrics.json) · [result](20261028-233704-s1_happy-glm-5.3-baseline-rep1/result.json) |
| [20261028-233713-s1_happy-glm-5.3-baseline-rep2](20261028-233713-s1_happy-glm-5.3-baseline-rep2/) | s1_happy | glm-5.3-baseline | green | 10.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233713-s1_happy-glm-5.3-baseline-rep2/metrics.json) · [result](20261028-233713-s1_happy-glm-5.3-baseline-rep2/result.json) |
| [20261028-233720-s1_happy-glm-5.3-baseline-rep3](20261028-233720-s1_happy-glm-5.3-baseline-rep3/) | s1_happy | glm-5.3-baseline | green | 10.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233720-s1_happy-glm-5.3-baseline-rep3/metrics.json) · [result](20261028-233720-s1_happy-glm-5.3-baseline-rep3/result.json) |
| [20261028-233722-s1_happy-glm-5.3-baseline-rep4](20261028-233722-s1_happy-glm-5.3-baseline-rep4/) | s1_happy | glm-5.3-baseline | green | 12.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233722-s1_happy-glm-5.3-baseline-rep4/metrics.json) · [result](20261028-233722-s1_happy-glm-5.3-baseline-rep4/result.json) |
| [20261028-233730-s1_happy-glm-5.3-baseline-rep5](20261028-233730-s1_happy-glm-5.3-baseline-rep5/) | s1_happy | glm-5.3-baseline | green | 15.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233730-s1_happy-glm-5.3-baseline-rep5/metrics.json) · [result](20261028-233730-s1_happy-glm-5.3-baseline-rep5/result.json) |
| [20261028-233736-s1_happy-glm-5.3-baseline-rep6](20261028-233736-s1_happy-glm-5.3-baseline-rep6/) | s1_happy | glm-5.3-baseline | green | 10.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233736-s1_happy-glm-5.3-baseline-rep6/metrics.json) · [result](20261028-233736-s1_happy-glm-5.3-baseline-rep6/result.json) |
| [20261028-233740-s1_happy-glm-5.3-baseline-rep7](20261028-233740-s1_happy-glm-5.3-baseline-rep7/) | s1_happy | glm-5.3-baseline | green | 9.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233740-s1_happy-glm-5.3-baseline-rep7/metrics.json) · [result](20261028-233740-s1_happy-glm-5.3-baseline-rep7/result.json) |
| [20261028-233752-s1_happy-glm-5.3-baseline-rep8](20261028-233752-s1_happy-glm-5.3-baseline-rep8/) | s1_happy | glm-5.3-baseline | green | 13.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233752-s1_happy-glm-5.3-baseline-rep8/metrics.json) · [result](20261028-233752-s1_happy-glm-5.3-baseline-rep8/result.json) |
| [20261028-233755-s1_happy-glm-5.3-baseline-rep9](20261028-233755-s1_happy-glm-5.3-baseline-rep9/) | s1_happy | glm-5.3-baseline | green | 14.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-233755-s1_happy-glm-5.3-baseline-rep9/metrics.json) · [result](20261028-233755-s1_happy-glm-5.3-baseline-rep9/result.json) |
| [20261028-234109-s1_happy-incredible-four-rep0](20261028-234109-s1_happy-incredible-four-rep0/) | s1_happy | incredible-four | green | 88.4 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-234109-s1_happy-incredible-four-rep0/metrics.json) · [result](20261028-234109-s1_happy-incredible-four-rep0/result.json) |
| [20261028-234113-s1_happy-incredible-four-rep1](20261028-234113-s1_happy-incredible-four-rep1/) | s1_happy | incredible-four | green | 118.4 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-234113-s1_happy-incredible-four-rep1/metrics.json) · [result](20261028-234113-s1_happy-incredible-four-rep1/result.json) |
| [20261028-234249-s1_happy-incredible-four-rep2](20261028-234249-s1_happy-incredible-four-rep2/) | s1_happy | incredible-four | green | 42.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-234249-s1_happy-incredible-four-rep2/metrics.json) · [result](20261028-234249-s1_happy-incredible-four-rep2/result.json) |
| [20261028-234318-s1_happy-incredible-four-rep3](20261028-234318-s1_happy-incredible-four-rep3/) | s1_happy | incredible-four | green | 36.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-234318-s1_happy-incredible-four-rep3/metrics.json) · [result](20261028-234318-s1_happy-incredible-four-rep3/result.json) |
| [20261028-234340-s1_happy-incredible-four-rep4](20261028-234340-s1_happy-incredible-four-rep4/) | s1_happy | incredible-four | green | 911.9 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | net-retry×5 | [metrics](20261028-234340-s1_happy-incredible-four-rep4/metrics.json) · [result](20261028-234340-s1_happy-incredible-four-rep4/result.json) |
| [20261028-234400-s1_happy-incredible-four-rep5](20261028-234400-s1_happy-incredible-four-rep5/) | s1_happy | incredible-four | green | 283.7 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-234400-s1_happy-incredible-four-rep5/metrics.json) · [result](20261028-234400-s1_happy-incredible-four-rep5/result.json) |
| [20261028-234420-s1_happy-incredible-four-rep6](20261028-234420-s1_happy-incredible-four-rep6/) | s1_happy | incredible-four | green | 65.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-234420-s1_happy-incredible-four-rep6/metrics.json) · [result](20261028-234420-s1_happy-incredible-four-rep6/result.json) |
| [20261028-234531-s1_happy-incredible-four-rep7](20261028-234531-s1_happy-incredible-four-rep7/) | s1_happy | incredible-four | green | 107.3 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-234531-s1_happy-incredible-four-rep7/metrics.json) · [result](20261028-234531-s1_happy-incredible-four-rep7/result.json) |
| [20261028-234730-s1_happy-incredible-four-rep8](20261028-234730-s1_happy-incredible-four-rep8/) | s1_happy | incredible-four | green | 687.5 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | net-retry | [metrics](20261028-234730-s1_happy-incredible-four-rep8/metrics.json) · [result](20261028-234730-s1_happy-incredible-four-rep8/result.json) |
| [20261028-234856-s1_happy-incredible-four-rep9](20261028-234856-s1_happy-incredible-four-rep9/) | s1_happy | incredible-four | green | 641.5 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | net-retry | [metrics](20261028-234856-s1_happy-incredible-four-rep9/metrics.json) · [result](20261028-234856-s1_happy-incredible-four-rep9/result.json) |
| [20261028-235902-s1_happy-regular-three-rep0](20261028-235902-s1_happy-regular-three-rep0/) | s1_happy | regular-three | green | 12.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-235902-s1_happy-regular-three-rep0/metrics.json) · [result](20261028-235902-s1_happy-regular-three-rep0/result.json) |
| [20261028-235908-s1_happy-regular-three-rep1](20261028-235908-s1_happy-regular-three-rep1/) | s1_happy | regular-three | green | 12.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-235908-s1_happy-regular-three-rep1/metrics.json) · [result](20261028-235908-s1_happy-regular-three-rep1/result.json) |
| [20261028-235926-s1_happy-regular-three-rep2](20261028-235926-s1_happy-regular-three-rep2/) | s1_happy | regular-three | green | 14.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-235926-s1_happy-regular-three-rep2/metrics.json) · [result](20261028-235926-s1_happy-regular-three-rep2/result.json) |
| [20261028-235927-s1_happy-regular-three-rep3](20261028-235927-s1_happy-regular-three-rep3/) | s1_happy | regular-three | green | 10.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-235927-s1_happy-regular-three-rep3/metrics.json) · [result](20261028-235927-s1_happy-regular-three-rep3/result.json) |
| [20261028-235943-s1_happy-regular-three-rep4](20261028-235943-s1_happy-regular-three-rep4/) | s1_happy | regular-three | green | 12.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-235943-s1_happy-regular-three-rep4/metrics.json) · [result](20261028-235943-s1_happy-regular-three-rep4/result.json) |
| [20261028-235947-s1_happy-regular-three-rep5](20261028-235947-s1_happy-regular-three-rep5/) | s1_happy | regular-three | green | 15.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-235947-s1_happy-regular-three-rep5/metrics.json) · [result](20261028-235947-s1_happy-regular-three-rep5/result.json) |
| [20261028-235947-s1_happy-regular-three-rep6](20261028-235947-s1_happy-regular-three-rep6/) | s1_happy | regular-three | green | 10.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261028-235947-s1_happy-regular-three-rep6/metrics.json) · [result](20261028-235947-s1_happy-regular-three-rep6/result.json) |
| [20261029-000003-s1_happy-regular-three-rep7](20261029-000003-s1_happy-regular-three-rep7/) | s1_happy | regular-three | green | 14.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-000003-s1_happy-regular-three-rep7/metrics.json) · [result](20261029-000003-s1_happy-regular-three-rep7/result.json) |
| [20261029-000003-s1_happy-regular-three-rep8](20261029-000003-s1_happy-regular-three-rep8/) | s1_happy | regular-three | green | 14.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-000003-s1_happy-regular-three-rep8/metrics.json) · [result](20261029-000003-s1_happy-regular-three-rep8/result.json) |
| [20261029-000008-s1_happy-regular-three-rep9](20261029-000008-s1_happy-regular-three-rep9/) | s1_happy | regular-three | green | 10.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-000008-s1_happy-regular-three-rep9/metrics.json) · [result](20261029-000008-s1_happy-regular-three-rep9/result.json) |
| [20261029-000301-s2a_bug_followup-deepseek-v4-baseline-rep0](20261029-000301-s2a_bug_followup-deepseek-v4-baseline-rep0/) | s2a_bug_followup | deepseek-v4-baseline | green | 205.7 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000301-s2a_bug_followup-deepseek-v4-baseline-rep0/metrics.json) · [result](20261029-000301-s2a_bug_followup-deepseek-v4-baseline-rep0/result.json) |
| [20261029-000309-s2a_bug_followup-deepseek-v4-baseline-rep1](20261029-000309-s2a_bug_followup-deepseek-v4-baseline-rep1/) | s2a_bug_followup | deepseek-v4-baseline | green | 166.5 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000309-s2a_bug_followup-deepseek-v4-baseline-rep1/metrics.json) · [result](20261029-000309-s2a_bug_followup-deepseek-v4-baseline-rep1/result.json) |
| [20261029-000336-s2a_bug_followup-deepseek-v4-baseline-rep2](20261029-000336-s2a_bug_followup-deepseek-v4-baseline-rep2/) | s2a_bug_followup | deepseek-v4-baseline | green | 220.7 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000336-s2a_bug_followup-deepseek-v4-baseline-rep2/metrics.json) · [result](20261029-000336-s2a_bug_followup-deepseek-v4-baseline-rep2/result.json) |
| [20261029-000601-s2a_bug_followup-deepseek-v4-baseline-rep3](20261029-000601-s2a_bug_followup-deepseek-v4-baseline-rep3/) | s2a_bug_followup | deepseek-v4-baseline | green | 202.6 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000601-s2a_bug_followup-deepseek-v4-baseline-rep3/metrics.json) · [result](20261029-000601-s2a_bug_followup-deepseek-v4-baseline-rep3/result.json) |
| [20261029-000632-s2a_bug_followup-deepseek-v4-baseline-rep4](20261029-000632-s2a_bug_followup-deepseek-v4-baseline-rep4/) | s2a_bug_followup | deepseek-v4-baseline | green | 158.6 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000632-s2a_bug_followup-deepseek-v4-baseline-rep4/metrics.json) · [result](20261029-000632-s2a_bug_followup-deepseek-v4-baseline-rep4/result.json) |
| [20261029-000722-s2a_bug_followup-deepseek-v4-baseline-rep5](20261029-000722-s2a_bug_followup-deepseek-v4-baseline-rep5/) | s2a_bug_followup | deepseek-v4-baseline | failed | 114.3 s | — | 0/0/0 | 2 | 1 ⚠ | bug:testing/bug:clarification | ok | stuck-clarif | [metrics](20261029-000722-s2a_bug_followup-deepseek-v4-baseline-rep5/metrics.json) · [result](20261029-000722-s2a_bug_followup-deepseek-v4-baseline-rep5/result.json) |
| [20261029-000917-s2a_bug_followup-deepseek-v4-baseline-rep6](20261029-000917-s2a_bug_followup-deepseek-v4-baseline-rep6/) | s2a_bug_followup | deepseek-v4-baseline | green | 138.4 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000917-s2a_bug_followup-deepseek-v4-baseline-rep6/metrics.json) · [result](20261029-000917-s2a_bug_followup-deepseek-v4-baseline-rep6/result.json) |
| [20261029-000928-s2a_bug_followup-deepseek-v4-baseline-rep7](20261029-000928-s2a_bug_followup-deepseek-v4-baseline-rep7/) | s2a_bug_followup | deepseek-v4-baseline | green | 192.5 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000928-s2a_bug_followup-deepseek-v4-baseline-rep7/metrics.json) · [result](20261029-000928-s2a_bug_followup-deepseek-v4-baseline-rep7/result.json) |
| [20261029-000933-s2a_bug_followup-deepseek-v4-baseline-rep8](20261029-000933-s2a_bug_followup-deepseek-v4-baseline-rep8/) | s2a_bug_followup | deepseek-v4-baseline | green | 168.5 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000933-s2a_bug_followup-deepseek-v4-baseline-rep8/metrics.json) · [result](20261029-000933-s2a_bug_followup-deepseek-v4-baseline-rep8/result.json) |
| [20261029-001145-s2a_bug_followup-deepseek-v4-baseline-rep9](20261029-001145-s2a_bug_followup-deepseek-v4-baseline-rep9/) | s2a_bug_followup | deepseek-v4-baseline | green | 191.6 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001145-s2a_bug_followup-deepseek-v4-baseline-rep9/metrics.json) · [result](20261029-001145-s2a_bug_followup-deepseek-v4-baseline-rep9/result.json) |
| [20261029-000026-s2a_bug_followup-glm-5.3-baseline-rep0](20261029-000026-s2a_bug_followup-glm-5.3-baseline-rep0/) | s2a_bug_followup | glm-5.3-baseline | green | 45.3 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000026-s2a_bug_followup-glm-5.3-baseline-rep0/metrics.json) · [result](20261029-000026-s2a_bug_followup-glm-5.3-baseline-rep0/result.json) |
| [20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep1](20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep1/) | s2a_bug_followup | glm-5.3-baseline | green | 41.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep1/metrics.json) · [result](20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep1/result.json) |
| [20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep2](20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep2/) | s2a_bug_followup | glm-5.3-baseline | green | 49.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep2/metrics.json) · [result](20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep2/result.json) |
| [20261029-000118-s2a_bug_followup-glm-5.3-baseline-rep3](20261029-000118-s2a_bug_followup-glm-5.3-baseline-rep3/) | s2a_bug_followup | glm-5.3-baseline | green | 33.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000118-s2a_bug_followup-glm-5.3-baseline-rep3/metrics.json) · [result](20261029-000118-s2a_bug_followup-glm-5.3-baseline-rep3/result.json) |
| [20261029-000119-s2a_bug_followup-glm-5.3-baseline-rep4](20261029-000119-s2a_bug_followup-glm-5.3-baseline-rep4/) | s2a_bug_followup | glm-5.3-baseline | green | 42.1 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000119-s2a_bug_followup-glm-5.3-baseline-rep4/metrics.json) · [result](20261029-000119-s2a_bug_followup-glm-5.3-baseline-rep4/result.json) |
| [20261029-000127-s2a_bug_followup-glm-5.3-baseline-rep5](20261029-000127-s2a_bug_followup-glm-5.3-baseline-rep5/) | s2a_bug_followup | glm-5.3-baseline | green | 41.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000127-s2a_bug_followup-glm-5.3-baseline-rep5/metrics.json) · [result](20261029-000127-s2a_bug_followup-glm-5.3-baseline-rep5/result.json) |
| [20261029-000201-s2a_bug_followup-glm-5.3-baseline-rep6](20261029-000201-s2a_bug_followup-glm-5.3-baseline-rep6/) | s2a_bug_followup | glm-5.3-baseline | green | 41.1 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000201-s2a_bug_followup-glm-5.3-baseline-rep6/metrics.json) · [result](20261029-000201-s2a_bug_followup-glm-5.3-baseline-rep6/result.json) |
| [20261029-000211-s2a_bug_followup-glm-5.3-baseline-rep7](20261029-000211-s2a_bug_followup-glm-5.3-baseline-rep7/) | s2a_bug_followup | glm-5.3-baseline | green | 43.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000211-s2a_bug_followup-glm-5.3-baseline-rep7/metrics.json) · [result](20261029-000211-s2a_bug_followup-glm-5.3-baseline-rep7/result.json) |
| [20261029-000214-s2a_bug_followup-glm-5.3-baseline-rep8](20261029-000214-s2a_bug_followup-glm-5.3-baseline-rep8/) | s2a_bug_followup | glm-5.3-baseline | green | 46.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000214-s2a_bug_followup-glm-5.3-baseline-rep8/metrics.json) · [result](20261029-000214-s2a_bug_followup-glm-5.3-baseline-rep8/result.json) |
| [20261029-000249-s2a_bug_followup-glm-5.3-baseline-rep9](20261029-000249-s2a_bug_followup-glm-5.3-baseline-rep9/) | s2a_bug_followup | glm-5.3-baseline | green | 36.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-000249-s2a_bug_followup-glm-5.3-baseline-rep9/metrics.json) · [result](20261029-000249-s2a_bug_followup-glm-5.3-baseline-rep9/result.json) |
| [20261029-001228-s2a_bug_followup-incredible-four-rep0](20261029-001228-s2a_bug_followup-incredible-four-rep0/) | s2a_bug_followup | incredible-four | green | 81.3 s | — | 0/0/0 | 3 | 2 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001228-s2a_bug_followup-incredible-four-rep0/metrics.json) · [result](20261029-001228-s2a_bug_followup-incredible-four-rep0/result.json) |
| [20261029-001247-s2a_bug_followup-incredible-four-rep1](20261029-001247-s2a_bug_followup-incredible-four-rep1/) | s2a_bug_followup | incredible-four | green | 74.3 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001247-s2a_bug_followup-incredible-four-rep1/metrics.json) · [result](20261029-001247-s2a_bug_followup-incredible-four-rep1/result.json) |
| [20261029-001356-s2a_bug_followup-incredible-four-rep2](20261029-001356-s2a_bug_followup-incredible-four-rep2/) | s2a_bug_followup | incredible-four | green | 90.4 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001356-s2a_bug_followup-incredible-four-rep2/metrics.json) · [result](20261029-001356-s2a_bug_followup-incredible-four-rep2/result.json) |
| [20261029-001411-s2a_bug_followup-incredible-four-rep3](20261029-001411-s2a_bug_followup-incredible-four-rep3/) | s2a_bug_followup | incredible-four | green | 71.3 s | — | 0/0/0 | 3 | 2 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001411-s2a_bug_followup-incredible-four-rep3/metrics.json) · [result](20261029-001411-s2a_bug_followup-incredible-four-rep3/result.json) |
| [20261029-001506-s2a_bug_followup-incredible-four-rep4](20261029-001506-s2a_bug_followup-incredible-four-rep4/) | s2a_bug_followup | incredible-four | green | 88.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001506-s2a_bug_followup-incredible-four-rep4/metrics.json) · [result](20261029-001506-s2a_bug_followup-incredible-four-rep4/result.json) |
| [20261029-001529-s2a_bug_followup-incredible-four-rep5](20261029-001529-s2a_bug_followup-incredible-four-rep5/) | s2a_bug_followup | incredible-four | green | 71.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001529-s2a_bug_followup-incredible-four-rep5/metrics.json) · [result](20261029-001529-s2a_bug_followup-incredible-four-rep5/result.json) |
| [20261029-001535-s2a_bug_followup-incredible-four-rep6](20261029-001535-s2a_bug_followup-incredible-four-rep6/) | s2a_bug_followup | incredible-four | green | 84.3 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001535-s2a_bug_followup-incredible-four-rep6/metrics.json) · [result](20261029-001535-s2a_bug_followup-incredible-four-rep6/result.json) |
| [20261029-001645-s2a_bug_followup-incredible-four-rep7](20261029-001645-s2a_bug_followup-incredible-four-rep7/) | s2a_bug_followup | incredible-four | green | 74.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001645-s2a_bug_followup-incredible-four-rep7/metrics.json) · [result](20261029-001645-s2a_bug_followup-incredible-four-rep7/result.json) |
| [20261029-001647-s2a_bug_followup-incredible-four-rep8](20261029-001647-s2a_bug_followup-incredible-four-rep8/) | s2a_bug_followup | incredible-four | green | 96.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001647-s2a_bug_followup-incredible-four-rep8/metrics.json) · [result](20261029-001647-s2a_bug_followup-incredible-four-rep8/result.json) |
| [20261029-001706-s2a_bug_followup-incredible-four-rep9](20261029-001706-s2a_bug_followup-incredible-four-rep9/) | s2a_bug_followup | incredible-four | green | 133.4 s | — | 0/0/0 | 4 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001706-s2a_bug_followup-incredible-four-rep9/metrics.json) · [result](20261029-001706-s2a_bug_followup-incredible-four-rep9/result.json) |
| [20261029-001811-s2a_bug_followup-regular-three-rep0](20261029-001811-s2a_bug_followup-regular-three-rep0/) | s2a_bug_followup | regular-three | green | 48.1 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001811-s2a_bug_followup-regular-three-rep0/metrics.json) · [result](20261029-001811-s2a_bug_followup-regular-three-rep0/result.json) |
| [20261029-001833-s2a_bug_followup-regular-three-rep1](20261029-001833-s2a_bug_followup-regular-three-rep1/) | s2a_bug_followup | regular-three | green | 41.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001833-s2a_bug_followup-regular-three-rep1/metrics.json) · [result](20261029-001833-s2a_bug_followup-regular-three-rep1/result.json) |
| [20261029-001909-s2a_bug_followup-regular-three-rep2](20261029-001909-s2a_bug_followup-regular-three-rep2/) | s2a_bug_followup | regular-three | green | 51.4 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001909-s2a_bug_followup-regular-three-rep2/metrics.json) · [result](20261029-001909-s2a_bug_followup-regular-three-rep2/result.json) |
| [20261029-001920-s2a_bug_followup-regular-three-rep3](20261029-001920-s2a_bug_followup-regular-three-rep3/) | s2a_bug_followup | regular-three | green | 50.3 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001920-s2a_bug_followup-regular-three-rep3/metrics.json) · [result](20261029-001920-s2a_bug_followup-regular-three-rep3/result.json) |
| [20261029-001926-s2a_bug_followup-regular-three-rep4](20261029-001926-s2a_bug_followup-regular-three-rep4/) | s2a_bug_followup | regular-three | green | 43.1 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-001926-s2a_bug_followup-regular-three-rep4/metrics.json) · [result](20261029-001926-s2a_bug_followup-regular-three-rep4/result.json) |
| [20261029-002006-s2a_bug_followup-regular-three-rep5](20261029-002006-s2a_bug_followup-regular-three-rep5/) | s2a_bug_followup | regular-three | green | 43.1 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002006-s2a_bug_followup-regular-three-rep5/metrics.json) · [result](20261029-002006-s2a_bug_followup-regular-three-rep5/result.json) |
| [20261029-002016-s2a_bug_followup-regular-three-rep6](20261029-002016-s2a_bug_followup-regular-three-rep6/) | s2a_bug_followup | regular-three | failed | 28.1 s | — | 0/0/0 | 2 | 1 ⚠ | bug:clarification/bug:testing | ok | stuck-clarif | [metrics](20261029-002016-s2a_bug_followup-regular-three-rep6/metrics.json) · [result](20261029-002016-s2a_bug_followup-regular-three-rep6/result.json) |
| [20261029-002021-s2a_bug_followup-regular-three-rep7](20261029-002021-s2a_bug_followup-regular-three-rep7/) | s2a_bug_followup | regular-three | green | 44.1 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002021-s2a_bug_followup-regular-three-rep7/metrics.json) · [result](20261029-002021-s2a_bug_followup-regular-three-rep7/result.json) |
| [20261029-002050-s2a_bug_followup-regular-three-rep8](20261029-002050-s2a_bug_followup-regular-three-rep8/) | s2a_bug_followup | regular-three | green | 42.2 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002050-s2a_bug_followup-regular-three-rep8/metrics.json) · [result](20261029-002050-s2a_bug_followup-regular-three-rep8/result.json) |
| [20261029-002056-s2a_bug_followup-regular-three-rep9](20261029-002056-s2a_bug_followup-regular-three-rep9/) | s2a_bug_followup | regular-three | green | 44.3 s | — | 0/0/0 | 3 | 1 | bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002056-s2a_bug_followup-regular-three-rep9/metrics.json) · [result](20261029-002056-s2a_bug_followup-regular-three-rep9/result.json) |
| [20261029-002433-s2b_bug_report-deepseek-v4-baseline-rep0](20261029-002433-s2b_bug_report-deepseek-v4-baseline-rep0/) | s2b_bug_report | deepseek-v4-baseline | green | 174.5 s | — | 0/0/0 | 3 | 0 | bug:Verified successfully/feature:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-002433-s2b_bug_report-deepseek-v4-baseline-rep0/metrics.json) · [result](20261029-002433-s2b_bug_report-deepseek-v4-baseline-rep0/result.json) |
| [20261029-002435-s2b_bug_report-deepseek-v4-baseline-rep1](20261029-002435-s2b_bug_report-deepseek-v4-baseline-rep1/) | s2b_bug_report | deepseek-v4-baseline | green | 226.6 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002435-s2b_bug_report-deepseek-v4-baseline-rep1/metrics.json) · [result](20261029-002435-s2b_bug_report-deepseek-v4-baseline-rep1/result.json) |
| [20261029-002459-s2b_bug_report-deepseek-v4-baseline-rep2](20261029-002459-s2b_bug_report-deepseek-v4-baseline-rep2/) | s2b_bug_report | deepseek-v4-baseline | green | 206.7 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002459-s2b_bug_report-deepseek-v4-baseline-rep2/metrics.json) · [result](20261029-002459-s2b_bug_report-deepseek-v4-baseline-rep2/result.json) |
| [20261029-002739-s2b_bug_report-deepseek-v4-baseline-rep3](20261029-002739-s2b_bug_report-deepseek-v4-baseline-rep3/) | s2b_bug_report | deepseek-v4-baseline | green | 384.1 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-002739-s2b_bug_report-deepseek-v4-baseline-rep3/metrics.json) · [result](20261029-002739-s2b_bug_report-deepseek-v4-baseline-rep3/result.json) |
| [20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep4](20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep4/) | s2b_bug_report | deepseek-v4-baseline | green | 207.6 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep4/metrics.json) · [result](20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep4/result.json) |
| [20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep5](20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep5/) | s2b_bug_report | deepseek-v4-baseline | green | 192.5 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep5/metrics.json) · [result](20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep5/result.json) |
| [20261029-003152-s2b_bug_report-deepseek-v4-baseline-rep6](20261029-003152-s2b_bug_report-deepseek-v4-baseline-rep6/) | s2b_bug_report | deepseek-v4-baseline | green | 183.7 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-003152-s2b_bug_report-deepseek-v4-baseline-rep6/metrics.json) · [result](20261029-003152-s2b_bug_report-deepseek-v4-baseline-rep6/result.json) |
| [20261029-003208-s2b_bug_report-deepseek-v4-baseline-rep7](20261029-003208-s2b_bug_report-deepseek-v4-baseline-rep7/) | s2b_bug_report | deepseek-v4-baseline | green | 168.5 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-003208-s2b_bug_report-deepseek-v4-baseline-rep7/metrics.json) · [result](20261029-003208-s2b_bug_report-deepseek-v4-baseline-rep7/result.json) |
| [20261029-003413-s2b_bug_report-deepseek-v4-baseline-rep8](20261029-003413-s2b_bug_report-deepseek-v4-baseline-rep8/) | s2b_bug_report | deepseek-v4-baseline | green | 232.7 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-003413-s2b_bug_report-deepseek-v4-baseline-rep8/metrics.json) · [result](20261029-003413-s2b_bug_report-deepseek-v4-baseline-rep8/result.json) |
| [20261029-003503-s2b_bug_report-deepseek-v4-baseline-rep9](20261029-003503-s2b_bug_report-deepseek-v4-baseline-rep9/) | s2b_bug_report | deepseek-v4-baseline | green | 182.6 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-003503-s2b_bug_report-deepseek-v4-baseline-rep9/metrics.json) · [result](20261029-003503-s2b_bug_report-deepseek-v4-baseline-rep9/result.json) |
| [20261029-002111-s2b_bug_report-glm-5.3-baseline-rep0](20261029-002111-s2b_bug_report-glm-5.3-baseline-rep0/) | s2b_bug_report | glm-5.3-baseline | green | 60.4 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002111-s2b_bug_report-glm-5.3-baseline-rep0/metrics.json) · [result](20261029-002111-s2b_bug_report-glm-5.3-baseline-rep0/result.json) |
| [20261029-002142-s2b_bug_report-glm-5.3-baseline-rep1](20261029-002142-s2b_bug_report-glm-5.3-baseline-rep1/) | s2b_bug_report | glm-5.3-baseline | green | 56.4 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-002142-s2b_bug_report-glm-5.3-baseline-rep1/metrics.json) · [result](20261029-002142-s2b_bug_report-glm-5.3-baseline-rep1/result.json) |
| [20261029-002147-s2b_bug_report-glm-5.3-baseline-rep2](20261029-002147-s2b_bug_report-glm-5.3-baseline-rep2/) | s2b_bug_report | glm-5.3-baseline | green | 42.2 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002147-s2b_bug_report-glm-5.3-baseline-rep2/metrics.json) · [result](20261029-002147-s2b_bug_report-glm-5.3-baseline-rep2/result.json) |
| [20261029-002219-s2b_bug_report-glm-5.3-baseline-rep3](20261029-002219-s2b_bug_report-glm-5.3-baseline-rep3/) | s2b_bug_report | glm-5.3-baseline | green | 48.3 s | — | 0/0/0 | 3 | 0 | bug:Verified successfully/feature:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-002219-s2b_bug_report-glm-5.3-baseline-rep3/metrics.json) · [result](20261029-002219-s2b_bug_report-glm-5.3-baseline-rep3/result.json) |
| [20261029-002236-s2b_bug_report-glm-5.3-baseline-rep4](20261029-002236-s2b_bug_report-glm-5.3-baseline-rep4/) | s2b_bug_report | glm-5.3-baseline | green | 50.3 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002236-s2b_bug_report-glm-5.3-baseline-rep4/metrics.json) · [result](20261029-002236-s2b_bug_report-glm-5.3-baseline-rep4/result.json) |
| [20261029-002246-s2b_bug_report-glm-5.3-baseline-rep5](20261029-002246-s2b_bug_report-glm-5.3-baseline-rep5/) | s2b_bug_report | glm-5.3-baseline | green | 46.2 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002246-s2b_bug_report-glm-5.3-baseline-rep5/metrics.json) · [result](20261029-002246-s2b_bug_report-glm-5.3-baseline-rep5/result.json) |
| [20261029-002317-s2b_bug_report-glm-5.3-baseline-rep6](20261029-002317-s2b_bug_report-glm-5.3-baseline-rep6/) | s2b_bug_report | glm-5.3-baseline | green | 45.4 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002317-s2b_bug_report-glm-5.3-baseline-rep6/metrics.json) · [result](20261029-002317-s2b_bug_report-glm-5.3-baseline-rep6/result.json) |
| [20261029-002333-s2b_bug_report-glm-5.3-baseline-rep7](20261029-002333-s2b_bug_report-glm-5.3-baseline-rep7/) | s2b_bug_report | glm-5.3-baseline | green | 52.3 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-002333-s2b_bug_report-glm-5.3-baseline-rep7/metrics.json) · [result](20261029-002333-s2b_bug_report-glm-5.3-baseline-rep7/result.json) |
| [20261029-002339-s2b_bug_report-glm-5.3-baseline-rep8](20261029-002339-s2b_bug_report-glm-5.3-baseline-rep8/) | s2b_bug_report | glm-5.3-baseline | green | 48.3 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-002339-s2b_bug_report-glm-5.3-baseline-rep8/metrics.json) · [result](20261029-002339-s2b_bug_report-glm-5.3-baseline-rep8/result.json) |
| [20261029-002411-s2b_bug_report-glm-5.3-baseline-rep9](20261029-002411-s2b_bug_report-glm-5.3-baseline-rep9/) | s2b_bug_report | glm-5.3-baseline | green | 42.2 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-002411-s2b_bug_report-glm-5.3-baseline-rep9/metrics.json) · [result](20261029-002411-s2b_bug_report-glm-5.3-baseline-rep9/result.json) |
| [20261029-003505-s2b_bug_report-incredible-four-rep0](20261029-003505-s2b_bug_report-incredible-four-rep0/) | s2b_bug_report | incredible-four | green | 96.2 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-003505-s2b_bug_report-incredible-four-rep0/metrics.json) · [result](20261029-003505-s2b_bug_report-incredible-four-rep0/result.json) |
| [20261029-003648-s2b_bug_report-incredible-four-rep1](20261029-003648-s2b_bug_report-incredible-four-rep1/) | s2b_bug_report | incredible-four | green | 116.3 s | — | 0/0/0 | 3 | 0 | bug:Verified successfully/feature:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-003648-s2b_bug_report-incredible-four-rep1/metrics.json) · [result](20261029-003648-s2b_bug_report-incredible-four-rep1/result.json) |
| [20261029-003812-s2b_bug_report-incredible-four-rep2](20261029-003812-s2b_bug_report-incredible-four-rep2/) | s2b_bug_report | incredible-four | green | 86.4 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-003812-s2b_bug_report-incredible-four-rep2/metrics.json) · [result](20261029-003812-s2b_bug_report-incredible-four-rep2/result.json) |
| [20261029-003816-s2b_bug_report-incredible-four-rep3](20261029-003816-s2b_bug_report-incredible-four-rep3/) | s2b_bug_report | incredible-four | green | 136.4 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-003816-s2b_bug_report-incredible-four-rep3/metrics.json) · [result](20261029-003816-s2b_bug_report-incredible-four-rep3/result.json) |
| [20261029-003858-s2b_bug_report-incredible-four-rep4](20261029-003858-s2b_bug_report-incredible-four-rep4/) | s2b_bug_report | incredible-four | green | 98.4 s | — | 0/0/0 | 3 | 0 | bug:Verified successfully/feature:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-003858-s2b_bug_report-incredible-four-rep4/metrics.json) · [result](20261029-003858-s2b_bug_report-incredible-four-rep4/result.json) |
| [20261029-003949-s2b_bug_report-incredible-four-rep5](20261029-003949-s2b_bug_report-incredible-four-rep5/) | s2b_bug_report | incredible-four | green | 99.2 s | — | 0/0/0 | 3 | 0 | bug:Verified successfully/feature:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-003949-s2b_bug_report-incredible-four-rep5/metrics.json) · [result](20261029-003949-s2b_bug_report-incredible-four-rep5/result.json) |
| [20261029-004040-s2b_bug_report-incredible-four-rep6](20261029-004040-s2b_bug_report-incredible-four-rep6/) | s2b_bug_report | incredible-four | green | 91.3 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-004040-s2b_bug_report-incredible-four-rep6/metrics.json) · [result](20261029-004040-s2b_bug_report-incredible-four-rep6/result.json) |
| [20261029-004043-s2b_bug_report-incredible-four-rep7](20261029-004043-s2b_bug_report-incredible-four-rep7/) | s2b_bug_report | incredible-four | green | 74.3 s | — | 0/0/0 | 3 | 0 | bug:Verified successfully/feature:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-004043-s2b_bug_report-incredible-four-rep7/metrics.json) · [result](20261029-004043-s2b_bug_report-incredible-four-rep7/result.json) |
| [20261029-004140-s2b_bug_report-incredible-four-rep8](20261029-004140-s2b_bug_report-incredible-four-rep8/) | s2b_bug_report | incredible-four | green | 92.4 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-004140-s2b_bug_report-incredible-four-rep8/metrics.json) · [result](20261029-004140-s2b_bug_report-incredible-four-rep8/result.json) |
| [20261029-004205-s2b_bug_report-incredible-four-rep9](20261029-004205-s2b_bug_report-incredible-four-rep9/) | s2b_bug_report | incredible-four | green | 89.3 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-004205-s2b_bug_report-incredible-four-rep9/metrics.json) · [result](20261029-004205-s2b_bug_report-incredible-four-rep9/result.json) |
| [20261029-004218-s2b_bug_report-regular-three-rep0](20261029-004218-s2b_bug_report-regular-three-rep0/) | s2b_bug_report | regular-three | green | 56.1 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-004218-s2b_bug_report-regular-three-rep0/metrics.json) · [result](20261029-004218-s2b_bug_report-regular-three-rep0/result.json) |
| [20261029-004320-s2b_bug_report-regular-three-rep1](20261029-004320-s2b_bug_report-regular-three-rep1/) | s2b_bug_report | regular-three | green | 62.4 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-004320-s2b_bug_report-regular-three-rep1/metrics.json) · [result](20261029-004320-s2b_bug_report-regular-three-rep1/result.json) |
| [20261029-004323-s2b_bug_report-regular-three-rep2](20261029-004323-s2b_bug_report-regular-three-rep2/) | s2b_bug_report | regular-three | green | 59.3 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-004323-s2b_bug_report-regular-three-rep2/metrics.json) · [result](20261029-004323-s2b_bug_report-regular-three-rep2/result.json) |
| [20261029-004341-s2b_bug_report-regular-three-rep3](20261029-004341-s2b_bug_report-regular-three-rep3/) | s2b_bug_report | regular-three | green | 55.2 s | — | 0/0/0 | 3 | 0 | bug:Verified successfully/feature:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-004341-s2b_bug_report-regular-three-rep3/metrics.json) · [result](20261029-004341-s2b_bug_report-regular-three-rep3/result.json) |
| [20261029-004430-s2b_bug_report-regular-three-rep4](20261029-004430-s2b_bug_report-regular-three-rep4/) | s2b_bug_report | regular-three | green | 70.2 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-004430-s2b_bug_report-regular-three-rep4/metrics.json) · [result](20261029-004430-s2b_bug_report-regular-three-rep4/result.json) |
| [20261029-004433-s2b_bug_report-regular-three-rep5](20261029-004433-s2b_bug_report-regular-three-rep5/) | s2b_bug_report | regular-three | green | 52.2 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-004433-s2b_bug_report-regular-three-rep5/metrics.json) · [result](20261029-004433-s2b_bug_report-regular-three-rep5/result.json) |
| [20261029-004443-s2b_bug_report-regular-three-rep6](20261029-004443-s2b_bug_report-regular-three-rep6/) | s2b_bug_report | regular-three | green | 61.3 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-004443-s2b_bug_report-regular-three-rep6/metrics.json) · [result](20261029-004443-s2b_bug_report-regular-three-rep6/result.json) |
| [20261029-004532-s2b_bug_report-regular-three-rep7](20261029-004532-s2b_bug_report-regular-three-rep7/) | s2b_bug_report | regular-three | green | 60.2 s | — | 0/0/0 | 3 | 0 | bug:Verified successfully/feature:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-004532-s2b_bug_report-regular-three-rep7/metrics.json) · [result](20261029-004532-s2b_bug_report-regular-three-rep7/result.json) |
| [20261029-004550-s2b_bug_report-regular-three-rep8](20261029-004550-s2b_bug_report-regular-three-rep8/) | s2b_bug_report | regular-three | green | 52.3 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-004550-s2b_bug_report-regular-three-rep8/metrics.json) · [result](20261029-004550-s2b_bug_report-regular-three-rep8/result.json) |
| [20261029-004551-s2b_bug_report-regular-three-rep9](20261029-004551-s2b_bug_report-regular-three-rep9/) | s2b_bug_report | regular-three | green | 53.3 s | — | 0/0/0 | 3 | 0 | bug:Verified successfully/feature:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-004551-s2b_bug_report-regular-three-rep9/metrics.json) · [result](20261029-004551-s2b_bug_report-regular-three-rep9/result.json) |
| [20261029-004954-s3_compaction_coder-deepseek-v4-baseline-rep0](20261029-004954-s3_compaction_coder-deepseek-v4-baseline-rep0/) | s3_compaction_coder | deepseek-v4-baseline | green | 215.5 s | — | 3/6/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004954-s3_compaction_coder-deepseek-v4-baseline-rep0/metrics.json) · [result](20261029-004954-s3_compaction_coder-deepseek-v4-baseline-rep0/result.json) |
| [20261029-005005-s3_compaction_coder-deepseek-v4-baseline-rep1](20261029-005005-s3_compaction_coder-deepseek-v4-baseline-rep1/) | s3_compaction_coder | deepseek-v4-baseline | green | 305.8 s | — | 3/6/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-005005-s3_compaction_coder-deepseek-v4-baseline-rep1/metrics.json) · [result](20261029-005005-s3_compaction_coder-deepseek-v4-baseline-rep1/result.json) |
| [20261029-005049-s3_compaction_coder-deepseek-v4-baseline-rep2](20261029-005049-s3_compaction_coder-deepseek-v4-baseline-rep2/) | s3_compaction_coder | deepseek-v4-baseline | green | 230.6 s | — | 3/6/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-005049-s3_compaction_coder-deepseek-v4-baseline-rep2/metrics.json) · [result](20261029-005049-s3_compaction_coder-deepseek-v4-baseline-rep2/result.json) |
| [20261029-005340-s3_compaction_coder-deepseek-v4-baseline-rep3](20261029-005340-s3_compaction_coder-deepseek-v4-baseline-rep3/) | s3_compaction_coder | deepseek-v4-baseline | green | 245.6 s | — | 3/6/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-005340-s3_compaction_coder-deepseek-v4-baseline-rep3/metrics.json) · [result](20261029-005340-s3_compaction_coder-deepseek-v4-baseline-rep3/result.json) |
| [20261029-005446-s3_compaction_coder-deepseek-v4-baseline-rep4](20261029-005446-s3_compaction_coder-deepseek-v4-baseline-rep4/) | s3_compaction_coder | deepseek-v4-baseline | green | 191.5 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-005446-s3_compaction_coder-deepseek-v4-baseline-rep4/metrics.json) · [result](20261029-005446-s3_compaction_coder-deepseek-v4-baseline-rep4/result.json) |
| [20261029-005517-s3_compaction_coder-deepseek-v4-baseline-rep5](20261029-005517-s3_compaction_coder-deepseek-v4-baseline-rep5/) | s3_compaction_coder | deepseek-v4-baseline | green | 289.7 s | — | 3/6/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-005517-s3_compaction_coder-deepseek-v4-baseline-rep5/metrics.json) · [result](20261029-005517-s3_compaction_coder-deepseek-v4-baseline-rep5/result.json) |
| [20261029-005756-s3_compaction_coder-deepseek-v4-baseline-rep6](20261029-005756-s3_compaction_coder-deepseek-v4-baseline-rep6/) | s3_compaction_coder | deepseek-v4-baseline | green | 206.5 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-005756-s3_compaction_coder-deepseek-v4-baseline-rep6/metrics.json) · [result](20261029-005756-s3_compaction_coder-deepseek-v4-baseline-rep6/result.json) |
| [20261029-005807-s3_compaction_coder-deepseek-v4-baseline-rep7](20261029-005807-s3_compaction_coder-deepseek-v4-baseline-rep7/) | s3_compaction_coder | deepseek-v4-baseline | green | 169.4 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-005807-s3_compaction_coder-deepseek-v4-baseline-rep7/metrics.json) · [result](20261029-005807-s3_compaction_coder-deepseek-v4-baseline-rep7/result.json) |
| [20261029-010012-s3_compaction_coder-deepseek-v4-baseline-rep8](20261029-010012-s3_compaction_coder-deepseek-v4-baseline-rep8/) | s3_compaction_coder | deepseek-v4-baseline | green | 219.5 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010012-s3_compaction_coder-deepseek-v4-baseline-rep8/metrics.json) · [result](20261029-010012-s3_compaction_coder-deepseek-v4-baseline-rep8/result.json) |
| [20261029-010102-s3_compaction_coder-deepseek-v4-baseline-rep9](20261029-010102-s3_compaction_coder-deepseek-v4-baseline-rep9/) | s3_compaction_coder | deepseek-v4-baseline | green | 218.6 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010102-s3_compaction_coder-deepseek-v4-baseline-rep9/metrics.json) · [result](20261029-010102-s3_compaction_coder-deepseek-v4-baseline-rep9/result.json) |
| [20261029-004642-s3_compaction_coder-glm-5.3-baseline-rep0](20261029-004642-s3_compaction_coder-glm-5.3-baseline-rep0/) | s3_compaction_coder | glm-5.3-baseline | green | 61.3 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004642-s3_compaction_coder-glm-5.3-baseline-rep0/metrics.json) · [result](20261029-004642-s3_compaction_coder-glm-5.3-baseline-rep0/result.json) |
| [20261029-004649-s3_compaction_coder-glm-5.3-baseline-rep1](20261029-004649-s3_compaction_coder-glm-5.3-baseline-rep1/) | s3_compaction_coder | glm-5.3-baseline | green | 54.1 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004649-s3_compaction_coder-glm-5.3-baseline-rep1/metrics.json) · [result](20261029-004649-s3_compaction_coder-glm-5.3-baseline-rep1/result.json) |
| [20261029-004652-s3_compaction_coder-glm-5.3-baseline-rep2](20261029-004652-s3_compaction_coder-glm-5.3-baseline-rep2/) | s3_compaction_coder | glm-5.3-baseline | green | 57.3 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004652-s3_compaction_coder-glm-5.3-baseline-rep2/metrics.json) · [result](20261029-004652-s3_compaction_coder-glm-5.3-baseline-rep2/result.json) |
| [20261029-004750-s3_compaction_coder-glm-5.3-baseline-rep3](20261029-004750-s3_compaction_coder-glm-5.3-baseline-rep3/) | s3_compaction_coder | glm-5.3-baseline | green | 51.1 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004750-s3_compaction_coder-glm-5.3-baseline-rep3/metrics.json) · [result](20261029-004750-s3_compaction_coder-glm-5.3-baseline-rep3/result.json) |
| [20261029-004753-s3_compaction_coder-glm-5.3-baseline-rep4](20261029-004753-s3_compaction_coder-glm-5.3-baseline-rep4/) | s3_compaction_coder | glm-5.3-baseline | green | 46.1 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004753-s3_compaction_coder-glm-5.3-baseline-rep4/metrics.json) · [result](20261029-004753-s3_compaction_coder-glm-5.3-baseline-rep4/result.json) |
| [20261029-004756-s3_compaction_coder-glm-5.3-baseline-rep5](20261029-004756-s3_compaction_coder-glm-5.3-baseline-rep5/) | s3_compaction_coder | glm-5.3-baseline | green | 49.2 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004756-s3_compaction_coder-glm-5.3-baseline-rep5/metrics.json) · [result](20261029-004756-s3_compaction_coder-glm-5.3-baseline-rep5/result.json) |
| [20261029-004846-s3_compaction_coder-glm-5.3-baseline-rep6](20261029-004846-s3_compaction_coder-glm-5.3-baseline-rep6/) | s3_compaction_coder | glm-5.3-baseline | green | 62.1 s | — | 3/6/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004846-s3_compaction_coder-glm-5.3-baseline-rep6/metrics.json) · [result](20261029-004846-s3_compaction_coder-glm-5.3-baseline-rep6/result.json) |
| [20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep7](20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep7/) | s3_compaction_coder | glm-5.3-baseline | green | 62.1 s | — | 3/6/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep7/metrics.json) · [result](20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep7/result.json) |
| [20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep8](20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep8/) | s3_compaction_coder | glm-5.3-baseline | green | 49.1 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep8/metrics.json) · [result](20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep8/result.json) |
| [20261029-004951-s3_compaction_coder-glm-5.3-baseline-rep9](20261029-004951-s3_compaction_coder-glm-5.3-baseline-rep9/) | s3_compaction_coder | glm-5.3-baseline | green | 51.2 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-004951-s3_compaction_coder-glm-5.3-baseline-rep9/metrics.json) · [result](20261029-004951-s3_compaction_coder-glm-5.3-baseline-rep9/result.json) |
| [20261029-010132-s3_compaction_coder-incredible-four-rep0](20261029-010132-s3_compaction_coder-incredible-four-rep0/) | s3_compaction_coder | incredible-four | green | 75.3 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010132-s3_compaction_coder-incredible-four-rep0/metrics.json) · [result](20261029-010132-s3_compaction_coder-incredible-four-rep0/result.json) |
| [20261029-010258-s3_compaction_coder-incredible-four-rep1](20261029-010258-s3_compaction_coder-incredible-four-rep1/) | s3_compaction_coder | incredible-four | green | 81.3 s | — | 3/6/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010258-s3_compaction_coder-incredible-four-rep1/metrics.json) · [result](20261029-010258-s3_compaction_coder-incredible-four-rep1/result.json) |
| [20261029-010403-s3_compaction_coder-incredible-four-rep2](20261029-010403-s3_compaction_coder-incredible-four-rep2/) | s3_compaction_coder | incredible-four | green | 72.2 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010403-s3_compaction_coder-incredible-four-rep2/metrics.json) · [result](20261029-010403-s3_compaction_coder-incredible-four-rep2/result.json) |
| [20261029-010431-s3_compaction_coder-incredible-four-rep3](20261029-010431-s3_compaction_coder-incredible-four-rep3/) | s3_compaction_coder | incredible-four | green | 66.2 s | — | 1/2/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010431-s3_compaction_coder-incredible-four-rep3/metrics.json) · [result](20261029-010431-s3_compaction_coder-incredible-four-rep3/result.json) |
| [20261029-010449-s3_compaction_coder-incredible-four-rep4](20261029-010449-s3_compaction_coder-incredible-four-rep4/) | s3_compaction_coder | incredible-four | green | 63.3 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010449-s3_compaction_coder-incredible-four-rep4/metrics.json) · [result](20261029-010449-s3_compaction_coder-incredible-four-rep4/result.json) |
| [20261029-010526-s3_compaction_coder-incredible-four-rep5](20261029-010526-s3_compaction_coder-incredible-four-rep5/) | s3_compaction_coder | incredible-four | green | 63.1 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010526-s3_compaction_coder-incredible-four-rep5/metrics.json) · [result](20261029-010526-s3_compaction_coder-incredible-four-rep5/result.json) |
| [20261029-010543-s3_compaction_coder-incredible-four-rep6](20261029-010543-s3_compaction_coder-incredible-four-rep6/) | s3_compaction_coder | incredible-four | green | 53.1 s | — | 1/2/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010543-s3_compaction_coder-incredible-four-rep6/metrics.json) · [result](20261029-010543-s3_compaction_coder-incredible-four-rep6/result.json) |
| [20261029-010558-s3_compaction_coder-incredible-four-rep7](20261029-010558-s3_compaction_coder-incredible-four-rep7/) | s3_compaction_coder | incredible-four | green | 66.2 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010558-s3_compaction_coder-incredible-four-rep7/metrics.json) · [result](20261029-010558-s3_compaction_coder-incredible-four-rep7/result.json) |
| [20261029-010640-s3_compaction_coder-incredible-four-rep8](20261029-010640-s3_compaction_coder-incredible-four-rep8/) | s3_compaction_coder | incredible-four | green | 64.2 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010640-s3_compaction_coder-incredible-four-rep8/metrics.json) · [result](20261029-010640-s3_compaction_coder-incredible-four-rep8/result.json) |
| [20261029-010642-s3_compaction_coder-incredible-four-rep9](20261029-010642-s3_compaction_coder-incredible-four-rep9/) | s3_compaction_coder | incredible-four | green | 63.3 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010642-s3_compaction_coder-incredible-four-rep9/metrics.json) · [result](20261029-010642-s3_compaction_coder-incredible-four-rep9/result.json) |
| [20261029-010710-s3_compaction_coder-regular-three-rep0](20261029-010710-s3_compaction_coder-regular-three-rep0/) | s3_compaction_coder | regular-three | green | 42.1 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010710-s3_compaction_coder-regular-three-rep0/metrics.json) · [result](20261029-010710-s3_compaction_coder-regular-three-rep0/result.json) |
| [20261029-010753-s3_compaction_coder-regular-three-rep1](20261029-010753-s3_compaction_coder-regular-three-rep1/) | s3_compaction_coder | regular-three | green | 32.1 s | — | 1/2/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010753-s3_compaction_coder-regular-three-rep1/metrics.json) · [result](20261029-010753-s3_compaction_coder-regular-three-rep1/result.json) |
| [20261029-010755-s3_compaction_coder-regular-three-rep2](20261029-010755-s3_compaction_coder-regular-three-rep2/) | s3_compaction_coder | regular-three | green | 44.1 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010755-s3_compaction_coder-regular-three-rep2/metrics.json) · [result](20261029-010755-s3_compaction_coder-regular-three-rep2/result.json) |
| [20261029-010759-s3_compaction_coder-regular-three-rep3](20261029-010759-s3_compaction_coder-regular-three-rep3/) | s3_compaction_coder | regular-three | green | 63.2 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010759-s3_compaction_coder-regular-three-rep3/metrics.json) · [result](20261029-010759-s3_compaction_coder-regular-three-rep3/result.json) |
| [20261029-010839-s3_compaction_coder-regular-three-rep4](20261029-010839-s3_compaction_coder-regular-three-rep4/) | s3_compaction_coder | regular-three | green | 33.1 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010839-s3_compaction_coder-regular-three-rep4/metrics.json) · [result](20261029-010839-s3_compaction_coder-regular-three-rep4/result.json) |
| [20261029-010851-s3_compaction_coder-regular-three-rep5](20261029-010851-s3_compaction_coder-regular-three-rep5/) | s3_compaction_coder | regular-three | green | 49.2 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010851-s3_compaction_coder-regular-three-rep5/metrics.json) · [result](20261029-010851-s3_compaction_coder-regular-three-rep5/result.json) |
| [20261029-010910-s3_compaction_coder-regular-three-rep6](20261029-010910-s3_compaction_coder-regular-three-rep6/) | s3_compaction_coder | regular-three | green | 45.1 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010910-s3_compaction_coder-regular-three-rep6/metrics.json) · [result](20261029-010910-s3_compaction_coder-regular-three-rep6/result.json) |
| [20261029-010918-s3_compaction_coder-regular-three-rep7](20261029-010918-s3_compaction_coder-regular-three-rep7/) | s3_compaction_coder | regular-three | green | 48.1 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010918-s3_compaction_coder-regular-three-rep7/metrics.json) · [result](20261029-010918-s3_compaction_coder-regular-three-rep7/result.json) |
| [20261029-010946-s3_compaction_coder-regular-three-rep8](20261029-010946-s3_compaction_coder-regular-three-rep8/) | s3_compaction_coder | regular-three | green | 50.3 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-010946-s3_compaction_coder-regular-three-rep8/metrics.json) · [result](20261029-010946-s3_compaction_coder-regular-three-rep8/result.json) |
| [20261029-011007-s3_compaction_coder-regular-three-rep9](20261029-011007-s3_compaction_coder-regular-three-rep9/) | s3_compaction_coder | regular-three | green | 53.4 s | — | 2/4/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-011007-s3_compaction_coder-regular-three-rep9/metrics.json) · [result](20261029-011007-s3_compaction_coder-regular-three-rep9/result.json) |
| [20261029-011528-s4_compaction_tester-deepseek-v4-baseline-rep0](20261029-011528-s4_compaction_tester-deepseek-v4-baseline-rep0/) | s4_compaction_tester | deepseek-v4-baseline | green | 331.8 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011528-s4_compaction_tester-deepseek-v4-baseline-rep0/metrics.json) · [result](20261029-011528-s4_compaction_tester-deepseek-v4-baseline-rep0/result.json) |
| [20261029-011640-s4_compaction_tester-deepseek-v4-baseline-rep1](20261029-011640-s4_compaction_tester-deepseek-v4-baseline-rep1/) | s4_compaction_tester | deepseek-v4-baseline | green | 272.7 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011640-s4_compaction_tester-deepseek-v4-baseline-rep1/metrics.json) · [result](20261029-011640-s4_compaction_tester-deepseek-v4-baseline-rep1/result.json) |
| [20261029-011652-s4_compaction_tester-deepseek-v4-baseline-rep2](20261029-011652-s4_compaction_tester-deepseek-v4-baseline-rep2/) | s4_compaction_tester | deepseek-v4-baseline | green | 287.7 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011652-s4_compaction_tester-deepseek-v4-baseline-rep2/metrics.json) · [result](20261029-011652-s4_compaction_tester-deepseek-v4-baseline-rep2/result.json) |
| [20261029-012107-s4_compaction_tester-deepseek-v4-baseline-rep3](20261029-012107-s4_compaction_tester-deepseek-v4-baseline-rep3/) | s4_compaction_tester | deepseek-v4-baseline | green | 216.5 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-012107-s4_compaction_tester-deepseek-v4-baseline-rep3/metrics.json) · [result](20261029-012107-s4_compaction_tester-deepseek-v4-baseline-rep3/result.json) |
| [20261029-012123-s4_compaction_tester-deepseek-v4-baseline-rep4](20261029-012123-s4_compaction_tester-deepseek-v4-baseline-rep4/) | s4_compaction_tester | deepseek-v4-baseline | green | 228.6 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-012123-s4_compaction_tester-deepseek-v4-baseline-rep4/metrics.json) · [result](20261029-012123-s4_compaction_tester-deepseek-v4-baseline-rep4/result.json) |
| [20261029-012145-s4_compaction_tester-deepseek-v4-baseline-rep5](20261029-012145-s4_compaction_tester-deepseek-v4-baseline-rep5/) | s4_compaction_tester | deepseek-v4-baseline | green | 219.5 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-012145-s4_compaction_tester-deepseek-v4-baseline-rep5/metrics.json) · [result](20261029-012145-s4_compaction_tester-deepseek-v4-baseline-rep5/result.json) |
| [20261029-012458-s4_compaction_tester-deepseek-v4-baseline-rep6](20261029-012458-s4_compaction_tester-deepseek-v4-baseline-rep6/) | s4_compaction_tester | deepseek-v4-baseline | green | 448.3 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-012458-s4_compaction_tester-deepseek-v4-baseline-rep6/metrics.json) · [result](20261029-012458-s4_compaction_tester-deepseek-v4-baseline-rep6/result.json) |
| [20261029-012518-s4_compaction_tester-deepseek-v4-baseline-rep7](20261029-012518-s4_compaction_tester-deepseek-v4-baseline-rep7/) | s4_compaction_tester | deepseek-v4-baseline | green | 350.9 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-012518-s4_compaction_tester-deepseek-v4-baseline-rep7/metrics.json) · [result](20261029-012518-s4_compaction_tester-deepseek-v4-baseline-rep7/result.json) |
| [20261029-012531-s4_compaction_tester-deepseek-v4-baseline-rep8](20261029-012531-s4_compaction_tester-deepseek-v4-baseline-rep8/) | s4_compaction_tester | deepseek-v4-baseline | green | 337.8 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-012531-s4_compaction_tester-deepseek-v4-baseline-rep8/metrics.json) · [result](20261029-012531-s4_compaction_tester-deepseek-v4-baseline-rep8/result.json) |
| [20261029-013115-s4_compaction_tester-deepseek-v4-baseline-rep9](20261029-013115-s4_compaction_tester-deepseek-v4-baseline-rep9/) | s4_compaction_tester | deepseek-v4-baseline | green | 269.7 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-013115-s4_compaction_tester-deepseek-v4-baseline-rep9/metrics.json) · [result](20261029-013115-s4_compaction_tester-deepseek-v4-baseline-rep9/result.json) |
| [20261029-011012-s4_compaction_tester-glm-5.3-baseline-rep0](20261029-011012-s4_compaction_tester-glm-5.3-baseline-rep0/) | s4_compaction_tester | glm-5.3-baseline | green | 89.3 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011012-s4_compaction_tester-glm-5.3-baseline-rep0/metrics.json) · [result](20261029-011012-s4_compaction_tester-glm-5.3-baseline-rep0/result.json) |
| [20261029-011042-s4_compaction_tester-glm-5.3-baseline-rep1](20261029-011042-s4_compaction_tester-glm-5.3-baseline-rep1/) | s4_compaction_tester | glm-5.3-baseline | green | 89.3 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011042-s4_compaction_tester-glm-5.3-baseline-rep1/metrics.json) · [result](20261029-011042-s4_compaction_tester-glm-5.3-baseline-rep1/result.json) |
| [20261029-011109-s4_compaction_tester-glm-5.3-baseline-rep2](20261029-011109-s4_compaction_tester-glm-5.3-baseline-rep2/) | s4_compaction_tester | glm-5.3-baseline | green | 115.4 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011109-s4_compaction_tester-glm-5.3-baseline-rep2/metrics.json) · [result](20261029-011109-s4_compaction_tester-glm-5.3-baseline-rep2/result.json) |
| [20261029-011150-s4_compaction_tester-glm-5.3-baseline-rep3](20261029-011150-s4_compaction_tester-glm-5.3-baseline-rep3/) | s4_compaction_tester | glm-5.3-baseline | green | 93.4 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011150-s4_compaction_tester-glm-5.3-baseline-rep3/metrics.json) · [result](20261029-011150-s4_compaction_tester-glm-5.3-baseline-rep3/result.json) |
| [20261029-011221-s4_compaction_tester-glm-5.3-baseline-rep4](20261029-011221-s4_compaction_tester-glm-5.3-baseline-rep4/) | s4_compaction_tester | glm-5.3-baseline | green | 85.3 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011221-s4_compaction_tester-glm-5.3-baseline-rep4/metrics.json) · [result](20261029-011221-s4_compaction_tester-glm-5.3-baseline-rep4/result.json) |
| [20261029-011311-s4_compaction_tester-glm-5.3-baseline-rep5](20261029-011311-s4_compaction_tester-glm-5.3-baseline-rep5/) | s4_compaction_tester | glm-5.3-baseline | green | 92.4 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011311-s4_compaction_tester-glm-5.3-baseline-rep5/metrics.json) · [result](20261029-011311-s4_compaction_tester-glm-5.3-baseline-rep5/result.json) |
| [20261029-011333-s4_compaction_tester-glm-5.3-baseline-rep6](20261029-011333-s4_compaction_tester-glm-5.3-baseline-rep6/) | s4_compaction_tester | glm-5.3-baseline | green | 92.3 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011333-s4_compaction_tester-glm-5.3-baseline-rep6/metrics.json) · [result](20261029-011333-s4_compaction_tester-glm-5.3-baseline-rep6/result.json) |
| [20261029-011352-s4_compaction_tester-glm-5.3-baseline-rep7](20261029-011352-s4_compaction_tester-glm-5.3-baseline-rep7/) | s4_compaction_tester | glm-5.3-baseline | green | 89.4 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011352-s4_compaction_tester-glm-5.3-baseline-rep7/metrics.json) · [result](20261029-011352-s4_compaction_tester-glm-5.3-baseline-rep7/result.json) |
| [20261029-011453-s4_compaction_tester-glm-5.3-baseline-rep8](20261029-011453-s4_compaction_tester-glm-5.3-baseline-rep8/) | s4_compaction_tester | glm-5.3-baseline | green | 96.4 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011453-s4_compaction_tester-glm-5.3-baseline-rep8/metrics.json) · [result](20261029-011453-s4_compaction_tester-glm-5.3-baseline-rep8/result.json) |
| [20261029-011513-s4_compaction_tester-glm-5.3-baseline-rep9](20261029-011513-s4_compaction_tester-glm-5.3-baseline-rep9/) | s4_compaction_tester | glm-5.3-baseline | green | 91.4 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-011513-s4_compaction_tester-glm-5.3-baseline-rep9/metrics.json) · [result](20261029-011513-s4_compaction_tester-glm-5.3-baseline-rep9/result.json) |
| [20261029-013116-s4_compaction_tester-incredible-four-rep0](20261029-013116-s4_compaction_tester-incredible-four-rep0/) | s4_compaction_tester | incredible-four | green | 277.8 s | — | 7/14/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-013116-s4_compaction_tester-incredible-four-rep0/metrics.json) · [result](20261029-013116-s4_compaction_tester-incredible-four-rep0/result.json) |
| [20261029-013236-s4_compaction_tester-incredible-four-rep1](20261029-013236-s4_compaction_tester-incredible-four-rep1/) | s4_compaction_tester | incredible-four | green | 345.1 s | — | 8/16/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-013236-s4_compaction_tester-incredible-four-rep1/metrics.json) · [result](20261029-013236-s4_compaction_tester-incredible-four-rep1/result.json) |
| [20261029-013555-s4_compaction_tester-incredible-four-rep2](20261029-013555-s4_compaction_tester-incredible-four-rep2/) | s4_compaction_tester | incredible-four | green | 248.8 s | — | 5/10/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-013555-s4_compaction_tester-incredible-four-rep2/metrics.json) · [result](20261029-013555-s4_compaction_tester-incredible-four-rep2/result.json) |
| [20261029-013603-s4_compaction_tester-incredible-four-rep3](20261029-013603-s4_compaction_tester-incredible-four-rep3/) | s4_compaction_tester | incredible-four | green | 144.6 s | — | 4/8/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-013603-s4_compaction_tester-incredible-four-rep3/metrics.json) · [result](20261029-013603-s4_compaction_tester-incredible-four-rep3/result.json) |
| [20261029-013835-s4_compaction_tester-incredible-four-rep4](20261029-013835-s4_compaction_tester-incredible-four-rep4/) | s4_compaction_tester | incredible-four | green | 468.5 s | — | 5/10/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-013835-s4_compaction_tester-incredible-four-rep4/metrics.json) · [result](20261029-013835-s4_compaction_tester-incredible-four-rep4/result.json) |
| [20261029-013835-s4_compaction_tester-incredible-four-rep5](20261029-013835-s4_compaction_tester-incredible-four-rep5/) | s4_compaction_tester | incredible-four | green | 1030.6 s | — | 5/10/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-013835-s4_compaction_tester-incredible-four-rep5/metrics.json) · [result](20261029-013835-s4_compaction_tester-incredible-four-rep5/result.json) |
| [20261029-014015-s4_compaction_tester-incredible-four-rep6](20261029-014015-s4_compaction_tester-incredible-four-rep6/) | s4_compaction_tester | incredible-four | green | 253.7 s | — | 4/8/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-014015-s4_compaction_tester-incredible-four-rep6/metrics.json) · [result](20261029-014015-s4_compaction_tester-incredible-four-rep6/result.json) |
| [20261029-014441-s4_compaction_tester-incredible-four-rep7](20261029-014441-s4_compaction_tester-incredible-four-rep7/) | s4_compaction_tester | incredible-four | green | 817.3 s | — | 7/14/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-014441-s4_compaction_tester-incredible-four-rep7/metrics.json) · [result](20261029-014441-s4_compaction_tester-incredible-four-rep7/result.json) |
| [20261029-014639-s4_compaction_tester-incredible-four-rep8](20261029-014639-s4_compaction_tester-incredible-four-rep8/) | s4_compaction_tester | incredible-four | green | 646.9 s | — | 5/10/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-014639-s4_compaction_tester-incredible-four-rep8/metrics.json) · [result](20261029-014639-s4_compaction_tester-incredible-four-rep8/result.json) |
| [20261029-015558-s4_compaction_tester-incredible-four-rep9](20261029-015558-s4_compaction_tester-incredible-four-rep9/) | s4_compaction_tester | incredible-four | green | 187.5 s | — | 5/10/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-015558-s4_compaction_tester-incredible-four-rep9/metrics.json) · [result](20261029-015558-s4_compaction_tester-incredible-four-rep9/result.json) |
| [20261029-015736-s4_compaction_tester-regular-three-rep0](20261029-015736-s4_compaction_tester-regular-three-rep0/) | s4_compaction_tester | regular-three | green | 103.3 s | — | 5/10/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-015736-s4_compaction_tester-regular-three-rep0/metrics.json) · [result](20261029-015736-s4_compaction_tester-regular-three-rep0/result.json) |
| [20261029-015828-s4_compaction_tester-regular-three-rep1](20261029-015828-s4_compaction_tester-regular-three-rep1/) | s4_compaction_tester | regular-three | green | 92.4 s | — | 6/12/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-015828-s4_compaction_tester-regular-three-rep1/metrics.json) · [result](20261029-015828-s4_compaction_tester-regular-three-rep1/result.json) |
| [20261029-015917-s4_compaction_tester-regular-three-rep2](20261029-015917-s4_compaction_tester-regular-three-rep2/) | s4_compaction_tester | regular-three | green | 191.5 s | — | 8/16/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-015917-s4_compaction_tester-regular-three-rep2/metrics.json) · [result](20261029-015917-s4_compaction_tester-regular-three-rep2/result.json) |
| [20261029-015930-s4_compaction_tester-regular-three-rep3](20261029-015930-s4_compaction_tester-regular-three-rep3/) | s4_compaction_tester | regular-three | green | 69.2 s | — | 2/4/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-015930-s4_compaction_tester-regular-three-rep3/metrics.json) · [result](20261029-015930-s4_compaction_tester-regular-three-rep3/result.json) |
| [20261029-020006-s4_compaction_tester-regular-three-rep4](20261029-020006-s4_compaction_tester-regular-three-rep4/) | s4_compaction_tester | regular-three | green | 86.3 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-020006-s4_compaction_tester-regular-three-rep4/metrics.json) · [result](20261029-020006-s4_compaction_tester-regular-three-rep4/result.json) |
| [20261029-020045-s4_compaction_tester-regular-three-rep5](20261029-020045-s4_compaction_tester-regular-three-rep5/) | s4_compaction_tester | regular-three | green | 82.2 s | — | 4/8/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-020045-s4_compaction_tester-regular-three-rep5/metrics.json) · [result](20261029-020045-s4_compaction_tester-regular-three-rep5/result.json) |
| [20261029-020140-s4_compaction_tester-regular-three-rep6](20261029-020140-s4_compaction_tester-regular-three-rep6/) | s4_compaction_tester | regular-three | green | 110.3 s | — | 6/12/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-020140-s4_compaction_tester-regular-three-rep6/metrics.json) · [result](20261029-020140-s4_compaction_tester-regular-three-rep6/result.json) |
| [20261029-020219-s4_compaction_tester-regular-three-rep7](20261029-020219-s4_compaction_tester-regular-three-rep7/) | s4_compaction_tester | regular-three | failed | 61.2 s | — | 2/4/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-020219-s4_compaction_tester-regular-three-rep7/metrics.json) · [result](20261029-020219-s4_compaction_tester-regular-three-rep7/result.json) |
| [20261029-020239-s4_compaction_tester-regular-three-rep8](20261029-020239-s4_compaction_tester-regular-three-rep8/) | s4_compaction_tester | regular-three | green | 92.4 s | — | 3/6/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-020239-s4_compaction_tester-regular-three-rep8/metrics.json) · [result](20261029-020239-s4_compaction_tester-regular-three-rep8/result.json) |
| [20261029-020332-s4_compaction_tester-regular-three-rep9](20261029-020332-s4_compaction_tester-regular-three-rep9/) | s4_compaction_tester | regular-three | green | 109.4 s | — | 4/8/0 | 1 | 0 | bug:Verified successfully | ok | clean | [metrics](20261029-020332-s4_compaction_tester-regular-three-rep9/metrics.json) · [result](20261029-020332-s4_compaction_tester-regular-three-rep9/result.json) |
| [20261029-020535-s5_clarification-deepseek-v4-baseline-rep0](20261029-020535-s5_clarification-deepseek-v4-baseline-rep0/) | s5_clarification | deepseek-v4-baseline | green | 65.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020535-s5_clarification-deepseek-v4-baseline-rep0/metrics.json) · [result](20261029-020535-s5_clarification-deepseek-v4-baseline-rep0/result.json) |
| [20261029-020550-s5_clarification-deepseek-v4-baseline-rep1](20261029-020550-s5_clarification-deepseek-v4-baseline-rep1/) | s5_clarification | deepseek-v4-baseline | green | 61.2 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020550-s5_clarification-deepseek-v4-baseline-rep1/metrics.json) · [result](20261029-020550-s5_clarification-deepseek-v4-baseline-rep1/result.json) |
| [20261029-020551-s5_clarification-deepseek-v4-baseline-rep2](20261029-020551-s5_clarification-deepseek-v4-baseline-rep2/) | s5_clarification | deepseek-v4-baseline | green | 67.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020551-s5_clarification-deepseek-v4-baseline-rep2/metrics.json) · [result](20261029-020551-s5_clarification-deepseek-v4-baseline-rep2/result.json) |
| [20261029-020645-s5_clarification-deepseek-v4-baseline-rep3](20261029-020645-s5_clarification-deepseek-v4-baseline-rep3/) | s5_clarification | deepseek-v4-baseline | green | 74.2 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020645-s5_clarification-deepseek-v4-baseline-rep3/metrics.json) · [result](20261029-020645-s5_clarification-deepseek-v4-baseline-rep3/result.json) |
| [20261029-020702-s5_clarification-deepseek-v4-baseline-rep4](20261029-020702-s5_clarification-deepseek-v4-baseline-rep4/) | s5_clarification | deepseek-v4-baseline | failed | 13.0 s | — | 0/0/0 | 0 | 0 ⚠ | feature:clarification | no-testing | stuck-clarif | [metrics](20261029-020702-s5_clarification-deepseek-v4-baseline-rep4/metrics.json) · [result](20261029-020702-s5_clarification-deepseek-v4-baseline-rep4/result.json) |
| [20261029-020708-s5_clarification-deepseek-v4-baseline-rep5](20261029-020708-s5_clarification-deepseek-v4-baseline-rep5/) | s5_clarification | deepseek-v4-baseline | green | 69.4 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020708-s5_clarification-deepseek-v4-baseline-rep5/metrics.json) · [result](20261029-020708-s5_clarification-deepseek-v4-baseline-rep5/result.json) |
| [20261029-020725-s5_clarification-deepseek-v4-baseline-rep6](20261029-020725-s5_clarification-deepseek-v4-baseline-rep6/) | s5_clarification | deepseek-v4-baseline | green | 62.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020725-s5_clarification-deepseek-v4-baseline-rep6/metrics.json) · [result](20261029-020725-s5_clarification-deepseek-v4-baseline-rep6/result.json) |
| [20261029-020804-s5_clarification-deepseek-v4-baseline-rep7](20261029-020804-s5_clarification-deepseek-v4-baseline-rep7/) | s5_clarification | deepseek-v4-baseline | green | 63.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020804-s5_clarification-deepseek-v4-baseline-rep7/metrics.json) · [result](20261029-020804-s5_clarification-deepseek-v4-baseline-rep7/result.json) |
| [20261029-020822-s5_clarification-deepseek-v4-baseline-rep8](20261029-020822-s5_clarification-deepseek-v4-baseline-rep8/) | s5_clarification | deepseek-v4-baseline | green | 52.2 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020822-s5_clarification-deepseek-v4-baseline-rep8/metrics.json) · [result](20261029-020822-s5_clarification-deepseek-v4-baseline-rep8/result.json) |
| [20261029-020833-s5_clarification-deepseek-v4-baseline-rep9](20261029-020833-s5_clarification-deepseek-v4-baseline-rep9/) | s5_clarification | deepseek-v4-baseline | green | 60.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020833-s5_clarification-deepseek-v4-baseline-rep9/metrics.json) · [result](20261029-020833-s5_clarification-deepseek-v4-baseline-rep9/result.json) |
| [20261029-020337-s5_clarification-glm-5.3-baseline-rep0](20261029-020337-s5_clarification-glm-5.3-baseline-rep0/) | s5_clarification | glm-5.3-baseline | green | 28.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020337-s5_clarification-glm-5.3-baseline-rep0/metrics.json) · [result](20261029-020337-s5_clarification-glm-5.3-baseline-rep0/result.json) |
| [20261029-020410-s5_clarification-glm-5.3-baseline-rep1](20261029-020410-s5_clarification-glm-5.3-baseline-rep1/) | s5_clarification | glm-5.3-baseline | green | 13.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020410-s5_clarification-glm-5.3-baseline-rep1/metrics.json) · [result](20261029-020410-s5_clarification-glm-5.3-baseline-rep1/result.json) |
| [20261029-020419-s5_clarification-glm-5.3-baseline-rep2](20261029-020419-s5_clarification-glm-5.3-baseline-rep2/) | s5_clarification | glm-5.3-baseline | green | 12.2 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020419-s5_clarification-glm-5.3-baseline-rep2/metrics.json) · [result](20261029-020419-s5_clarification-glm-5.3-baseline-rep2/result.json) |
| [20261029-020427-s5_clarification-glm-5.3-baseline-rep3](20261029-020427-s5_clarification-glm-5.3-baseline-rep3/) | s5_clarification | glm-5.3-baseline | green | 14.0 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020427-s5_clarification-glm-5.3-baseline-rep3/metrics.json) · [result](20261029-020427-s5_clarification-glm-5.3-baseline-rep3/result.json) |
| [20261029-020436-s5_clarification-glm-5.3-baseline-rep4](20261029-020436-s5_clarification-glm-5.3-baseline-rep4/) | s5_clarification | glm-5.3-baseline | green | 20.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020436-s5_clarification-glm-5.3-baseline-rep4/metrics.json) · [result](20261029-020436-s5_clarification-glm-5.3-baseline-rep4/result.json) |
| [20261029-020446-s5_clarification-glm-5.3-baseline-rep5](20261029-020446-s5_clarification-glm-5.3-baseline-rep5/) | s5_clarification | glm-5.3-baseline | green | 22.2 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020446-s5_clarification-glm-5.3-baseline-rep5/metrics.json) · [result](20261029-020446-s5_clarification-glm-5.3-baseline-rep5/result.json) |
| [20261029-020505-s5_clarification-glm-5.3-baseline-rep6](20261029-020505-s5_clarification-glm-5.3-baseline-rep6/) | s5_clarification | glm-5.3-baseline | green | 22.0 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020505-s5_clarification-glm-5.3-baseline-rep6/metrics.json) · [result](20261029-020505-s5_clarification-glm-5.3-baseline-rep6/result.json) |
| [20261029-020515-s5_clarification-glm-5.3-baseline-rep7](20261029-020515-s5_clarification-glm-5.3-baseline-rep7/) | s5_clarification | glm-5.3-baseline | green | 15.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020515-s5_clarification-glm-5.3-baseline-rep7/metrics.json) · [result](20261029-020515-s5_clarification-glm-5.3-baseline-rep7/result.json) |
| [20261029-020531-s5_clarification-glm-5.3-baseline-rep8](20261029-020531-s5_clarification-glm-5.3-baseline-rep8/) | s5_clarification | glm-5.3-baseline | green | 14.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020531-s5_clarification-glm-5.3-baseline-rep8/metrics.json) · [result](20261029-020531-s5_clarification-glm-5.3-baseline-rep8/result.json) |
| [20261029-020531-s5_clarification-glm-5.3-baseline-rep9](20261029-020531-s5_clarification-glm-5.3-baseline-rep9/) | s5_clarification | glm-5.3-baseline | green | 15.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020531-s5_clarification-glm-5.3-baseline-rep9/metrics.json) · [result](20261029-020531-s5_clarification-glm-5.3-baseline-rep9/result.json) |
| [20261029-020919-s5_clarification-incredible-four-rep0](20261029-020919-s5_clarification-incredible-four-rep0/) | s5_clarification | incredible-four | green | 25.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020919-s5_clarification-incredible-four-rep0/metrics.json) · [result](20261029-020919-s5_clarification-incredible-four-rep0/result.json) |
| [20261029-020920-s5_clarification-incredible-four-rep1](20261029-020920-s5_clarification-incredible-four-rep1/) | s5_clarification | incredible-four | green | 27.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020920-s5_clarification-incredible-four-rep1/metrics.json) · [result](20261029-020920-s5_clarification-incredible-four-rep1/result.json) |
| [20261029-020938-s5_clarification-incredible-four-rep2](20261029-020938-s5_clarification-incredible-four-rep2/) | s5_clarification | incredible-four | green | 31.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020938-s5_clarification-incredible-four-rep2/metrics.json) · [result](20261029-020938-s5_clarification-incredible-four-rep2/result.json) |
| [20261029-020956-s5_clarification-incredible-four-rep3](20261029-020956-s5_clarification-incredible-four-rep3/) | s5_clarification | incredible-four | green | 36.2 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020956-s5_clarification-incredible-four-rep3/metrics.json) · [result](20261029-020956-s5_clarification-incredible-four-rep3/result.json) |
| [20261029-020958-s5_clarification-incredible-four-rep4](20261029-020958-s5_clarification-incredible-four-rep4/) | s5_clarification | incredible-four | green | 39.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-020958-s5_clarification-incredible-four-rep4/metrics.json) · [result](20261029-020958-s5_clarification-incredible-four-rep4/result.json) |
| [20261029-021014-s5_clarification-incredible-four-rep5](20261029-021014-s5_clarification-incredible-four-rep5/) | s5_clarification | incredible-four | green | 31.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021014-s5_clarification-incredible-four-rep5/metrics.json) · [result](20261029-021014-s5_clarification-incredible-four-rep5/result.json) |
| [20261029-021038-s5_clarification-incredible-four-rep6](20261029-021038-s5_clarification-incredible-four-rep6/) | s5_clarification | incredible-four | green | 53.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021038-s5_clarification-incredible-four-rep6/metrics.json) · [result](20261029-021038-s5_clarification-incredible-four-rep6/result.json) |
| [20261029-021043-s5_clarification-incredible-four-rep7](20261029-021043-s5_clarification-incredible-four-rep7/) | s5_clarification | incredible-four | green | 32.2 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021043-s5_clarification-incredible-four-rep7/metrics.json) · [result](20261029-021043-s5_clarification-incredible-four-rep7/result.json) |
| [20261029-021050-s5_clarification-incredible-four-rep8](20261029-021050-s5_clarification-incredible-four-rep8/) | s5_clarification | incredible-four | green | 34.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021050-s5_clarification-incredible-four-rep8/metrics.json) · [result](20261029-021050-s5_clarification-incredible-four-rep8/result.json) |
| [20261029-021120-s5_clarification-incredible-four-rep9](20261029-021120-s5_clarification-incredible-four-rep9/) | s5_clarification | incredible-four | green | 39.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021120-s5_clarification-incredible-four-rep9/metrics.json) · [result](20261029-021120-s5_clarification-incredible-four-rep9/result.json) |
| [20261029-021129-s5_clarification-regular-three-rep0](20261029-021129-s5_clarification-regular-three-rep0/) | s5_clarification | regular-three | green | 16.0 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021129-s5_clarification-regular-three-rep0/metrics.json) · [result](20261029-021129-s5_clarification-regular-three-rep0/result.json) |
| [20261029-021141-s5_clarification-regular-three-rep1](20261029-021141-s5_clarification-regular-three-rep1/) | s5_clarification | regular-three | green | 15.0 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021141-s5_clarification-regular-three-rep1/metrics.json) · [result](20261029-021141-s5_clarification-regular-three-rep1/result.json) |
| [20261029-021151-s5_clarification-regular-three-rep2](20261029-021151-s5_clarification-regular-three-rep2/) | s5_clarification | regular-three | green | 16.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021151-s5_clarification-regular-three-rep2/metrics.json) · [result](20261029-021151-s5_clarification-regular-three-rep2/result.json) |
| [20261029-021204-s5_clarification-regular-three-rep3](20261029-021204-s5_clarification-regular-three-rep3/) | s5_clarification | regular-three | green | 37.1 s | — | 0/0/0 | 2 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021204-s5_clarification-regular-three-rep3/metrics.json) · [result](20261029-021204-s5_clarification-regular-three-rep3/result.json) |
| [20261029-021205-s5_clarification-regular-three-rep4](20261029-021205-s5_clarification-regular-three-rep4/) | s5_clarification | regular-three | green | 20.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021205-s5_clarification-regular-three-rep4/metrics.json) · [result](20261029-021205-s5_clarification-regular-three-rep4/result.json) |
| [20261029-021212-s5_clarification-regular-three-rep5](20261029-021212-s5_clarification-regular-three-rep5/) | s5_clarification | regular-three | green | 19.2 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021212-s5_clarification-regular-three-rep5/metrics.json) · [result](20261029-021212-s5_clarification-regular-three-rep5/result.json) |
| [20261029-021230-s5_clarification-regular-three-rep6](20261029-021230-s5_clarification-regular-three-rep6/) | s5_clarification | regular-three | green | 21.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021230-s5_clarification-regular-three-rep6/metrics.json) · [result](20261029-021230-s5_clarification-regular-three-rep6/result.json) |
| [20261029-021236-s5_clarification-regular-three-rep7](20261029-021236-s5_clarification-regular-three-rep7/) | s5_clarification | regular-three | green | 19.1 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021236-s5_clarification-regular-three-rep7/metrics.json) · [result](20261029-021236-s5_clarification-regular-three-rep7/result.json) |
| [20261029-021246-s5_clarification-regular-three-rep8](20261029-021246-s5_clarification-regular-three-rep8/) | s5_clarification | regular-three | green | 16.3 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021246-s5_clarification-regular-three-rep8/metrics.json) · [result](20261029-021246-s5_clarification-regular-three-rep8/result.json) |
| [20261029-021258-s5_clarification-regular-three-rep9](20261029-021258-s5_clarification-regular-three-rep9/) | s5_clarification | regular-three | green | 21.2 s | — | 0/0/0 | 1 | 1 | feature:Verified successfully | ok | clean | [metrics](20261029-021258-s5_clarification-regular-three-rep9/metrics.json) · [result](20261029-021258-s5_clarification-regular-three-rep9/result.json) |
| [20261029-021507-s6_queue_priority-deepseek-v4-baseline-rep0](20261029-021507-s6_queue_priority-deepseek-v4-baseline-rep0/) | s6_queue_priority | deepseek-v4-baseline | green | 95.4 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-021507-s6_queue_priority-deepseek-v4-baseline-rep0/metrics.json) · [result](20261029-021507-s6_queue_priority-deepseek-v4-baseline-rep0/result.json) |
| [20261029-021514-s6_queue_priority-deepseek-v4-baseline-rep1](20261029-021514-s6_queue_priority-deepseek-v4-baseline-rep1/) | s6_queue_priority | deepseek-v4-baseline | green | 67.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-021514-s6_queue_priority-deepseek-v4-baseline-rep1/metrics.json) · [result](20261029-021514-s6_queue_priority-deepseek-v4-baseline-rep1/result.json) |
| [20261029-021520-s6_queue_priority-deepseek-v4-baseline-rep2](20261029-021520-s6_queue_priority-deepseek-v4-baseline-rep2/) | s6_queue_priority | deepseek-v4-baseline | green | 103.4 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021520-s6_queue_priority-deepseek-v4-baseline-rep2/metrics.json) · [result](20261029-021520-s6_queue_priority-deepseek-v4-baseline-rep2/result.json) |
| [20261029-021628-s6_queue_priority-deepseek-v4-baseline-rep3](20261029-021628-s6_queue_priority-deepseek-v4-baseline-rep3/) | s6_queue_priority | deepseek-v4-baseline | green | 87.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-021628-s6_queue_priority-deepseek-v4-baseline-rep3/metrics.json) · [result](20261029-021628-s6_queue_priority-deepseek-v4-baseline-rep3/result.json) |
| [20261029-021653-s6_queue_priority-deepseek-v4-baseline-rep4](20261029-021653-s6_queue_priority-deepseek-v4-baseline-rep4/) | s6_queue_priority | deepseek-v4-baseline | green | 62.3 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021653-s6_queue_priority-deepseek-v4-baseline-rep4/metrics.json) · [result](20261029-021653-s6_queue_priority-deepseek-v4-baseline-rep4/result.json) |
| [20261029-021710-s6_queue_priority-deepseek-v4-baseline-rep5](20261029-021710-s6_queue_priority-deepseek-v4-baseline-rep5/) | s6_queue_priority | deepseek-v4-baseline | green | 75.3 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021710-s6_queue_priority-deepseek-v4-baseline-rep5/metrics.json) · [result](20261029-021710-s6_queue_priority-deepseek-v4-baseline-rep5/result.json) |
| [20261029-021802-s6_queue_priority-deepseek-v4-baseline-rep6](20261029-021802-s6_queue_priority-deepseek-v4-baseline-rep6/) | s6_queue_priority | deepseek-v4-baseline | green | 79.3 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021802-s6_queue_priority-deepseek-v4-baseline-rep6/metrics.json) · [result](20261029-021802-s6_queue_priority-deepseek-v4-baseline-rep6/result.json) |
| [20261029-021806-s6_queue_priority-deepseek-v4-baseline-rep7](20261029-021806-s6_queue_priority-deepseek-v4-baseline-rep7/) | s6_queue_priority | deepseek-v4-baseline | green | 65.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-021806-s6_queue_priority-deepseek-v4-baseline-rep7/metrics.json) · [result](20261029-021806-s6_queue_priority-deepseek-v4-baseline-rep7/result.json) |
| [20261029-021831-s6_queue_priority-deepseek-v4-baseline-rep8](20261029-021831-s6_queue_priority-deepseek-v4-baseline-rep8/) | s6_queue_priority | deepseek-v4-baseline | green | 62.3 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021831-s6_queue_priority-deepseek-v4-baseline-rep8/metrics.json) · [result](20261029-021831-s6_queue_priority-deepseek-v4-baseline-rep8/result.json) |
| [20261029-021918-s6_queue_priority-deepseek-v4-baseline-rep9](20261029-021918-s6_queue_priority-deepseek-v4-baseline-rep9/) | s6_queue_priority | deepseek-v4-baseline | green | 89.3 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021918-s6_queue_priority-deepseek-v4-baseline-rep9/metrics.json) · [result](20261029-021918-s6_queue_priority-deepseek-v4-baseline-rep9/result.json) |
| [20261029-021300-s6_queue_priority-glm-5.3-baseline-rep0](20261029-021300-s6_queue_priority-glm-5.3-baseline-rep0/) | s6_queue_priority | glm-5.3-baseline | green | 25.1 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021300-s6_queue_priority-glm-5.3-baseline-rep0/metrics.json) · [result](20261029-021300-s6_queue_priority-glm-5.3-baseline-rep0/result.json) |
| [20261029-021311-s6_queue_priority-glm-5.3-baseline-rep1](20261029-021311-s6_queue_priority-glm-5.3-baseline-rep1/) | s6_queue_priority | glm-5.3-baseline | green | 32.2 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021311-s6_queue_priority-glm-5.3-baseline-rep1/metrics.json) · [result](20261029-021311-s6_queue_priority-glm-5.3-baseline-rep1/result.json) |
| [20261029-021323-s6_queue_priority-glm-5.3-baseline-rep2](20261029-021323-s6_queue_priority-glm-5.3-baseline-rep2/) | s6_queue_priority | glm-5.3-baseline | green | 34.1 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021323-s6_queue_priority-glm-5.3-baseline-rep2/metrics.json) · [result](20261029-021323-s6_queue_priority-glm-5.3-baseline-rep2/result.json) |
| [20261029-021331-s6_queue_priority-glm-5.3-baseline-rep3](20261029-021331-s6_queue_priority-glm-5.3-baseline-rep3/) | s6_queue_priority | glm-5.3-baseline | green | 29.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-021331-s6_queue_priority-glm-5.3-baseline-rep3/metrics.json) · [result](20261029-021331-s6_queue_priority-glm-5.3-baseline-rep3/result.json) |
| [20261029-021351-s6_queue_priority-glm-5.3-baseline-rep4](20261029-021351-s6_queue_priority-glm-5.3-baseline-rep4/) | s6_queue_priority | glm-5.3-baseline | green | 29.1 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021351-s6_queue_priority-glm-5.3-baseline-rep4/metrics.json) · [result](20261029-021351-s6_queue_priority-glm-5.3-baseline-rep4/result.json) |
| [20261029-021404-s6_queue_priority-glm-5.3-baseline-rep5](20261029-021404-s6_queue_priority-glm-5.3-baseline-rep5/) | s6_queue_priority | glm-5.3-baseline | green | 26.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-021404-s6_queue_priority-glm-5.3-baseline-rep5/metrics.json) · [result](20261029-021404-s6_queue_priority-glm-5.3-baseline-rep5/result.json) |
| [20261029-021407-s6_queue_priority-glm-5.3-baseline-rep6](20261029-021407-s6_queue_priority-glm-5.3-baseline-rep6/) | s6_queue_priority | glm-5.3-baseline | green | 31.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-021407-s6_queue_priority-glm-5.3-baseline-rep6/metrics.json) · [result](20261029-021407-s6_queue_priority-glm-5.3-baseline-rep6/result.json) |
| [20261029-021432-s6_queue_priority-glm-5.3-baseline-rep7](20261029-021432-s6_queue_priority-glm-5.3-baseline-rep7/) | s6_queue_priority | glm-5.3-baseline | green | 27.1 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021432-s6_queue_priority-glm-5.3-baseline-rep7/metrics.json) · [result](20261029-021432-s6_queue_priority-glm-5.3-baseline-rep7/result.json) |
| [20261029-021437-s6_queue_priority-glm-5.3-baseline-rep8](20261029-021437-s6_queue_priority-glm-5.3-baseline-rep8/) | s6_queue_priority | glm-5.3-baseline | green | 30.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-021437-s6_queue_priority-glm-5.3-baseline-rep8/metrics.json) · [result](20261029-021437-s6_queue_priority-glm-5.3-baseline-rep8/result.json) |
| [20261029-021444-s6_queue_priority-glm-5.3-baseline-rep9](20261029-021444-s6_queue_priority-glm-5.3-baseline-rep9/) | s6_queue_priority | glm-5.3-baseline | green | 30.2 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-021444-s6_queue_priority-glm-5.3-baseline-rep9/metrics.json) · [result](20261029-021444-s6_queue_priority-glm-5.3-baseline-rep9/result.json) |
| [20261029-021932-s6_queue_priority-incredible-four-rep0](20261029-021932-s6_queue_priority-incredible-four-rep0/) | s6_queue_priority | incredible-four | green | 42.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-021932-s6_queue_priority-incredible-four-rep0/metrics.json) · [result](20261029-021932-s6_queue_priority-incredible-four-rep0/result.json) |
| [20261029-021940-s6_queue_priority-incredible-four-rep1](20261029-021940-s6_queue_priority-incredible-four-rep1/) | s6_queue_priority | incredible-four | green | 54.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-021940-s6_queue_priority-incredible-four-rep1/metrics.json) · [result](20261029-021940-s6_queue_priority-incredible-four-rep1/result.json) |
| [20261029-022021-s6_queue_priority-incredible-four-rep2](20261029-022021-s6_queue_priority-incredible-four-rep2/) | s6_queue_priority | incredible-four | green | 103.5 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-022021-s6_queue_priority-incredible-four-rep2/metrics.json) · [result](20261029-022021-s6_queue_priority-incredible-four-rep2/result.json) |
| [20261029-022040-s6_queue_priority-incredible-four-rep3](20261029-022040-s6_queue_priority-incredible-four-rep3/) | s6_queue_priority | incredible-four | green | 97.4 s | — | 0/0/0 | 3 | 0 | bug:Verified successfully/feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-022040-s6_queue_priority-incredible-four-rep3/metrics.json) · [result](20261029-022040-s6_queue_priority-incredible-four-rep3/result.json) |
| [20261029-022058-s6_queue_priority-incredible-four-rep4](20261029-022058-s6_queue_priority-incredible-four-rep4/) | s6_queue_priority | incredible-four | green | 87.3 s | — | 0/0/0 | 3 | 0 | feature:Verified successfully/bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-022058-s6_queue_priority-incredible-four-rep4/metrics.json) · [result](20261029-022058-s6_queue_priority-incredible-four-rep4/result.json) |
| [20261029-022214-s6_queue_priority-incredible-four-rep5](20261029-022214-s6_queue_priority-incredible-four-rep5/) | s6_queue_priority | incredible-four | green | 51.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-022214-s6_queue_priority-incredible-four-rep5/metrics.json) · [result](20261029-022214-s6_queue_priority-incredible-four-rep5/result.json) |
| [20261029-022224-s6_queue_priority-incredible-four-rep6](20261029-022224-s6_queue_priority-incredible-four-rep6/) | s6_queue_priority | incredible-four | green | 50.3 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-022224-s6_queue_priority-incredible-four-rep6/metrics.json) · [result](20261029-022224-s6_queue_priority-incredible-four-rep6/result.json) |
| [20261029-022231-s6_queue_priority-incredible-four-rep7](20261029-022231-s6_queue_priority-incredible-four-rep7/) | s6_queue_priority | incredible-four | green | 68.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-022231-s6_queue_priority-incredible-four-rep7/metrics.json) · [result](20261029-022231-s6_queue_priority-incredible-four-rep7/result.json) |
| [20261029-022316-s6_queue_priority-incredible-four-rep8](20261029-022316-s6_queue_priority-incredible-four-rep8/) | s6_queue_priority | incredible-four | green | 61.2 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-022316-s6_queue_priority-incredible-four-rep8/metrics.json) · [result](20261029-022316-s6_queue_priority-incredible-four-rep8/result.json) |
| [20261029-022322-s6_queue_priority-incredible-four-rep9](20261029-022322-s6_queue_priority-incredible-four-rep9/) | s6_queue_priority | incredible-four | green | 50.2 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-022322-s6_queue_priority-incredible-four-rep9/metrics.json) · [result](20261029-022322-s6_queue_priority-incredible-four-rep9/result.json) |
| [20261029-022347-s6_queue_priority-regular-three-rep0](20261029-022347-s6_queue_priority-regular-three-rep0/) | s6_queue_priority | regular-three | green | 26.1 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-022347-s6_queue_priority-regular-three-rep0/metrics.json) · [result](20261029-022347-s6_queue_priority-regular-three-rep0/result.json) |
| [20261029-022419-s6_queue_priority-regular-three-rep1](20261029-022419-s6_queue_priority-regular-three-rep1/) | s6_queue_priority | regular-three | green | 30.2 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-022419-s6_queue_priority-regular-three-rep1/metrics.json) · [result](20261029-022419-s6_queue_priority-regular-three-rep1/result.json) |
| [20261029-022419-s6_queue_priority-regular-three-rep2](20261029-022419-s6_queue_priority-regular-three-rep2/) | s6_queue_priority | regular-three | green | 30.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-022419-s6_queue_priority-regular-three-rep2/metrics.json) · [result](20261029-022419-s6_queue_priority-regular-three-rep2/result.json) |
| [20261029-022427-s6_queue_priority-regular-three-rep3](20261029-022427-s6_queue_priority-regular-three-rep3/) | s6_queue_priority | regular-three | failed | 33.1 s | — | 0/0/0 | 2 | 0 ⚠ | feature:testing/bug:Verified successfully/bug:clarification | ok | stuck-clarif | [metrics](20261029-022427-s6_queue_priority-regular-three-rep3/metrics.json) · [result](20261029-022427-s6_queue_priority-regular-three-rep3/result.json) |
| [20261029-022500-s6_queue_priority-regular-three-rep4](20261029-022500-s6_queue_priority-regular-three-rep4/) | s6_queue_priority | regular-three | green | 32.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-022500-s6_queue_priority-regular-three-rep4/metrics.json) · [result](20261029-022500-s6_queue_priority-regular-three-rep4/result.json) |
| [20261029-022500-s6_queue_priority-regular-three-rep5](20261029-022500-s6_queue_priority-regular-three-rep5/) | s6_queue_priority | regular-three | green | 33.3 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-022500-s6_queue_priority-regular-three-rep5/metrics.json) · [result](20261029-022500-s6_queue_priority-regular-three-rep5/result.json) |
| [20261029-022508-s6_queue_priority-regular-three-rep6](20261029-022508-s6_queue_priority-regular-three-rep6/) | s6_queue_priority | regular-three | green | 30.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-022508-s6_queue_priority-regular-three-rep6/metrics.json) · [result](20261029-022508-s6_queue_priority-regular-three-rep6/result.json) |
| [20261029-022541-s6_queue_priority-regular-three-rep7](20261029-022541-s6_queue_priority-regular-three-rep7/) | s6_queue_priority | regular-three | green | 30.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-022541-s6_queue_priority-regular-three-rep7/metrics.json) · [result](20261029-022541-s6_queue_priority-regular-three-rep7/result.json) |
| [20261029-022543-s6_queue_priority-regular-three-rep8](20261029-022543-s6_queue_priority-regular-three-rep8/) | s6_queue_priority | regular-three | green | 27.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261029-022543-s6_queue_priority-regular-three-rep8/metrics.json) · [result](20261029-022543-s6_queue_priority-regular-three-rep8/result.json) |
| [20261029-022545-s6_queue_priority-regular-three-rep9](20261029-022545-s6_queue_priority-regular-three-rep9/) | s6_queue_priority | regular-three | green | 26.1 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/feature:Verified successfully | ok | clean | [metrics](20261029-022545-s6_queue_priority-regular-three-rep9/metrics.json) · [result](20261029-022545-s6_queue_priority-regular-three-rep9/result.json) |
| [20261029-022813-s7_fault_injection-deepseek-v4-baseline-rep0](20261029-022813-s7_fault_injection-deepseek-v4-baseline-rep0/) | s7_fault_injection | deepseek-v4-baseline | green | 38.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022813-s7_fault_injection-deepseek-v4-baseline-rep0/metrics.json) · [result](20261029-022813-s7_fault_injection-deepseek-v4-baseline-rep0/result.json) |
| [20261029-022814-s7_fault_injection-deepseek-v4-baseline-rep1](20261029-022814-s7_fault_injection-deepseek-v4-baseline-rep1/) | s7_fault_injection | deepseek-v4-baseline | green | 38.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022814-s7_fault_injection-deepseek-v4-baseline-rep1/metrics.json) · [result](20261029-022814-s7_fault_injection-deepseek-v4-baseline-rep1/result.json) |
| [20261029-022851-s7_fault_injection-deepseek-v4-baseline-rep2](20261029-022851-s7_fault_injection-deepseek-v4-baseline-rep2/) | s7_fault_injection | deepseek-v4-baseline | green | 37.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022851-s7_fault_injection-deepseek-v4-baseline-rep2/metrics.json) · [result](20261029-022851-s7_fault_injection-deepseek-v4-baseline-rep2/result.json) |
| [20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep3](20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep3/) | s7_fault_injection | deepseek-v4-baseline | green | 45.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep3/metrics.json) · [result](20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep3/result.json) |
| [20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep4](20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep4/) | s7_fault_injection | deepseek-v4-baseline | green | 45.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep4/metrics.json) · [result](20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep4/result.json) |
| [20261029-022935-s7_fault_injection-deepseek-v4-baseline-rep5](20261029-022935-s7_fault_injection-deepseek-v4-baseline-rep5/) | s7_fault_injection | deepseek-v4-baseline | green | 54.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022935-s7_fault_injection-deepseek-v4-baseline-rep5/metrics.json) · [result](20261029-022935-s7_fault_injection-deepseek-v4-baseline-rep5/result.json) |
| [20261029-022954-s7_fault_injection-deepseek-v4-baseline-rep6](20261029-022954-s7_fault_injection-deepseek-v4-baseline-rep6/) | s7_fault_injection | deepseek-v4-baseline | green | 53.3 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022954-s7_fault_injection-deepseek-v4-baseline-rep6/metrics.json) · [result](20261029-022954-s7_fault_injection-deepseek-v4-baseline-rep6/result.json) |
| [20261029-022955-s7_fault_injection-deepseek-v4-baseline-rep7](20261029-022955-s7_fault_injection-deepseek-v4-baseline-rep7/) | s7_fault_injection | deepseek-v4-baseline | green | 47.3 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022955-s7_fault_injection-deepseek-v4-baseline-rep7/metrics.json) · [result](20261029-022955-s7_fault_injection-deepseek-v4-baseline-rep7/result.json) |
| [20261029-023040-s7_fault_injection-deepseek-v4-baseline-rep8](20261029-023040-s7_fault_injection-deepseek-v4-baseline-rep8/) | s7_fault_injection | deepseek-v4-baseline | green | 41.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023040-s7_fault_injection-deepseek-v4-baseline-rep8/metrics.json) · [result](20261029-023040-s7_fault_injection-deepseek-v4-baseline-rep8/result.json) |
| [20261029-023049-s7_fault_injection-deepseek-v4-baseline-rep9](20261029-023049-s7_fault_injection-deepseek-v4-baseline-rep9/) | s7_fault_injection | deepseek-v4-baseline | green | 48.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023049-s7_fault_injection-deepseek-v4-baseline-rep9/metrics.json) · [result](20261029-023049-s7_fault_injection-deepseek-v4-baseline-rep9/result.json) |
| [20261029-022619-s7_fault_injection-glm-5.3-baseline-rep0](20261029-022619-s7_fault_injection-glm-5.3-baseline-rep0/) | s7_fault_injection | glm-5.3-baseline | green | 28.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022619-s7_fault_injection-glm-5.3-baseline-rep0/metrics.json) · [result](20261029-022619-s7_fault_injection-glm-5.3-baseline-rep0/result.json) |
| [20261029-022620-s7_fault_injection-glm-5.3-baseline-rep1](20261029-022620-s7_fault_injection-glm-5.3-baseline-rep1/) | s7_fault_injection | glm-5.3-baseline | green | 30.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022620-s7_fault_injection-glm-5.3-baseline-rep1/metrics.json) · [result](20261029-022620-s7_fault_injection-glm-5.3-baseline-rep1/result.json) |
| [20261029-022623-s7_fault_injection-glm-5.3-baseline-rep2](20261029-022623-s7_fault_injection-glm-5.3-baseline-rep2/) | s7_fault_injection | glm-5.3-baseline | green | 28.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022623-s7_fault_injection-glm-5.3-baseline-rep2/metrics.json) · [result](20261029-022623-s7_fault_injection-glm-5.3-baseline-rep2/result.json) |
| [20261029-022657-s7_fault_injection-glm-5.3-baseline-rep3](20261029-022657-s7_fault_injection-glm-5.3-baseline-rep3/) | s7_fault_injection | glm-5.3-baseline | green | 29.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022657-s7_fault_injection-glm-5.3-baseline-rep3/metrics.json) · [result](20261029-022657-s7_fault_injection-glm-5.3-baseline-rep3/result.json) |
| [20261029-022659-s7_fault_injection-glm-5.3-baseline-rep4](20261029-022659-s7_fault_injection-glm-5.3-baseline-rep4/) | s7_fault_injection | glm-5.3-baseline | green | 29.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022659-s7_fault_injection-glm-5.3-baseline-rep4/metrics.json) · [result](20261029-022659-s7_fault_injection-glm-5.3-baseline-rep4/result.json) |
| [20261029-022700-s7_fault_injection-glm-5.3-baseline-rep5](20261029-022700-s7_fault_injection-glm-5.3-baseline-rep5/) | s7_fault_injection | glm-5.3-baseline | green | 29.3 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022700-s7_fault_injection-glm-5.3-baseline-rep5/metrics.json) · [result](20261029-022700-s7_fault_injection-glm-5.3-baseline-rep5/result.json) |
| [20261029-022737-s7_fault_injection-glm-5.3-baseline-rep6](20261029-022737-s7_fault_injection-glm-5.3-baseline-rep6/) | s7_fault_injection | glm-5.3-baseline | green | 31.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022737-s7_fault_injection-glm-5.3-baseline-rep6/metrics.json) · [result](20261029-022737-s7_fault_injection-glm-5.3-baseline-rep6/result.json) |
| [20261029-022737-s7_fault_injection-glm-5.3-baseline-rep7](20261029-022737-s7_fault_injection-glm-5.3-baseline-rep7/) | s7_fault_injection | glm-5.3-baseline | green | 30.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022737-s7_fault_injection-glm-5.3-baseline-rep7/metrics.json) · [result](20261029-022737-s7_fault_injection-glm-5.3-baseline-rep7/result.json) |
| [20261029-022737-s7_fault_injection-glm-5.3-baseline-rep8](20261029-022737-s7_fault_injection-glm-5.3-baseline-rep8/) | s7_fault_injection | glm-5.3-baseline | green | 29.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022737-s7_fault_injection-glm-5.3-baseline-rep8/metrics.json) · [result](20261029-022737-s7_fault_injection-glm-5.3-baseline-rep8/result.json) |
| [20261029-022812-s7_fault_injection-glm-5.3-baseline-rep9](20261029-022812-s7_fault_injection-glm-5.3-baseline-rep9/) | s7_fault_injection | glm-5.3-baseline | green | 28.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-022812-s7_fault_injection-glm-5.3-baseline-rep9/metrics.json) · [result](20261029-022812-s7_fault_injection-glm-5.3-baseline-rep9/result.json) |
| [20261029-023055-s7_fault_injection-incredible-four-rep0](20261029-023055-s7_fault_injection-incredible-four-rep0/) | s7_fault_injection | incredible-four | green | 39.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023055-s7_fault_injection-incredible-four-rep0/metrics.json) · [result](20261029-023055-s7_fault_injection-incredible-four-rep0/result.json) |
| [20261029-023131-s7_fault_injection-incredible-four-rep1](20261029-023131-s7_fault_injection-incredible-four-rep1/) | s7_fault_injection | incredible-four | green | 40.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023131-s7_fault_injection-incredible-four-rep1/metrics.json) · [result](20261029-023131-s7_fault_injection-incredible-four-rep1/result.json) |
| [20261029-023141-s7_fault_injection-incredible-four-rep2](20261029-023141-s7_fault_injection-incredible-four-rep2/) | s7_fault_injection | incredible-four | green | 34.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023141-s7_fault_injection-incredible-four-rep2/metrics.json) · [result](20261029-023141-s7_fault_injection-incredible-four-rep2/result.json) |
| [20261029-023143-s7_fault_injection-incredible-four-rep3](20261029-023143-s7_fault_injection-incredible-four-rep3/) | s7_fault_injection | incredible-four | green | 36.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023143-s7_fault_injection-incredible-four-rep3/metrics.json) · [result](20261029-023143-s7_fault_injection-incredible-four-rep3/result.json) |
| [20261029-023218-s7_fault_injection-incredible-four-rep4](20261029-023218-s7_fault_injection-incredible-four-rep4/) | s7_fault_injection | incredible-four | green | 33.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023218-s7_fault_injection-incredible-four-rep4/metrics.json) · [result](20261029-023218-s7_fault_injection-incredible-four-rep4/result.json) |
| [20261029-023225-s7_fault_injection-incredible-four-rep5](20261029-023225-s7_fault_injection-incredible-four-rep5/) | s7_fault_injection | incredible-four | green | 33.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023225-s7_fault_injection-incredible-four-rep5/metrics.json) · [result](20261029-023225-s7_fault_injection-incredible-four-rep5/result.json) |
| [20261029-023227-s7_fault_injection-incredible-four-rep6](20261029-023227-s7_fault_injection-incredible-four-rep6/) | s7_fault_injection | incredible-four | green | 35.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023227-s7_fault_injection-incredible-four-rep6/metrics.json) · [result](20261029-023227-s7_fault_injection-incredible-four-rep6/result.json) |
| [20261029-023257-s7_fault_injection-incredible-four-rep7](20261029-023257-s7_fault_injection-incredible-four-rep7/) | s7_fault_injection | incredible-four | green | 33.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023257-s7_fault_injection-incredible-four-rep7/metrics.json) · [result](20261029-023257-s7_fault_injection-incredible-four-rep7/result.json) |
| [20261029-023305-s7_fault_injection-incredible-four-rep8](20261029-023305-s7_fault_injection-incredible-four-rep8/) | s7_fault_injection | incredible-four | green | 33.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023305-s7_fault_injection-incredible-four-rep8/metrics.json) · [result](20261029-023305-s7_fault_injection-incredible-four-rep8/result.json) |
| [20261029-023308-s7_fault_injection-incredible-four-rep9](20261029-023308-s7_fault_injection-incredible-four-rep9/) | s7_fault_injection | incredible-four | green | 32.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023308-s7_fault_injection-incredible-four-rep9/metrics.json) · [result](20261029-023308-s7_fault_injection-incredible-four-rep9/result.json) |
| [20261029-023342-s7_fault_injection-regular-three-rep0](20261029-023342-s7_fault_injection-regular-three-rep0/) | s7_fault_injection | regular-three | green | 28.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023342-s7_fault_injection-regular-three-rep0/metrics.json) · [result](20261029-023342-s7_fault_injection-regular-three-rep0/result.json) |
| [20261029-023345-s7_fault_injection-regular-three-rep1](20261029-023345-s7_fault_injection-regular-three-rep1/) | s7_fault_injection | regular-three | green | 28.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023345-s7_fault_injection-regular-three-rep1/metrics.json) · [result](20261029-023345-s7_fault_injection-regular-three-rep1/result.json) |
| [20261029-023348-s7_fault_injection-regular-three-rep2](20261029-023348-s7_fault_injection-regular-three-rep2/) | s7_fault_injection | regular-three | green | 27.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023348-s7_fault_injection-regular-three-rep2/metrics.json) · [result](20261029-023348-s7_fault_injection-regular-three-rep2/result.json) |
| [20261029-023417-s7_fault_injection-regular-three-rep3](20261029-023417-s7_fault_injection-regular-three-rep3/) | s7_fault_injection | regular-three | green | 29.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023417-s7_fault_injection-regular-three-rep3/metrics.json) · [result](20261029-023417-s7_fault_injection-regular-three-rep3/result.json) |
| [20261029-023421-s7_fault_injection-regular-three-rep4](20261029-023421-s7_fault_injection-regular-three-rep4/) | s7_fault_injection | regular-three | green | 28.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023421-s7_fault_injection-regular-three-rep4/metrics.json) · [result](20261029-023421-s7_fault_injection-regular-three-rep4/result.json) |
| [20261029-023422-s7_fault_injection-regular-three-rep5](20261029-023422-s7_fault_injection-regular-three-rep5/) | s7_fault_injection | regular-three | green | 29.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023422-s7_fault_injection-regular-three-rep5/metrics.json) · [result](20261029-023422-s7_fault_injection-regular-three-rep5/result.json) |
| [20261029-023458-s7_fault_injection-regular-three-rep6](20261029-023458-s7_fault_injection-regular-three-rep6/) | s7_fault_injection | regular-three | green | 30.3 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023458-s7_fault_injection-regular-three-rep6/metrics.json) · [result](20261029-023458-s7_fault_injection-regular-three-rep6/result.json) |
| [20261029-023458-s7_fault_injection-regular-three-rep7](20261029-023458-s7_fault_injection-regular-three-rep7/) | s7_fault_injection | regular-three | green | 29.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023458-s7_fault_injection-regular-three-rep7/metrics.json) · [result](20261029-023458-s7_fault_injection-regular-three-rep7/result.json) |
| [20261029-023459-s7_fault_injection-regular-three-rep8](20261029-023459-s7_fault_injection-regular-three-rep8/) | s7_fault_injection | regular-three | green | 29.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023459-s7_fault_injection-regular-three-rep8/metrics.json) · [result](20261029-023459-s7_fault_injection-regular-three-rep8/result.json) |
| [20261029-023536-s7_fault_injection-regular-three-rep9](20261029-023536-s7_fault_injection-regular-three-rep9/) | s7_fault_injection | regular-three | green | 28.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | faults×5, net-retry×3 | [metrics](20261029-023536-s7_fault_injection-regular-three-rep9/metrics.json) · [result](20261029-023536-s7_fault_injection-regular-three-rep9/result.json) |
| [20261029-023744-s8_fix_loop-deepseek-v4-baseline-rep0](20261029-023744-s8_fix_loop-deepseek-v4-baseline-rep0/) | s8_fix_loop | deepseek-v4-baseline | green | 109.5 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023744-s8_fix_loop-deepseek-v4-baseline-rep0/metrics.json) · [result](20261029-023744-s8_fix_loop-deepseek-v4-baseline-rep0/result.json) |
| [20261029-023806-s8_fix_loop-deepseek-v4-baseline-rep1](20261029-023806-s8_fix_loop-deepseek-v4-baseline-rep1/) | s8_fix_loop | deepseek-v4-baseline | green | 90.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023806-s8_fix_loop-deepseek-v4-baseline-rep1/metrics.json) · [result](20261029-023806-s8_fix_loop-deepseek-v4-baseline-rep1/result.json) |
| [20261029-023810-s8_fix_loop-deepseek-v4-baseline-rep2](20261029-023810-s8_fix_loop-deepseek-v4-baseline-rep2/) | s8_fix_loop | deepseek-v4-baseline | green | 129.5 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023810-s8_fix_loop-deepseek-v4-baseline-rep2/metrics.json) · [result](20261029-023810-s8_fix_loop-deepseek-v4-baseline-rep2/result.json) |
| [20261029-023939-s8_fix_loop-deepseek-v4-baseline-rep3](20261029-023939-s8_fix_loop-deepseek-v4-baseline-rep3/) | s8_fix_loop | deepseek-v4-baseline | green | 135.4 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023939-s8_fix_loop-deepseek-v4-baseline-rep3/metrics.json) · [result](20261029-023939-s8_fix_loop-deepseek-v4-baseline-rep3/result.json) |
| [20261029-023947-s8_fix_loop-deepseek-v4-baseline-rep4](20261029-023947-s8_fix_loop-deepseek-v4-baseline-rep4/) | s8_fix_loop | deepseek-v4-baseline | green | 119.4 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023947-s8_fix_loop-deepseek-v4-baseline-rep4/metrics.json) · [result](20261029-023947-s8_fix_loop-deepseek-v4-baseline-rep4/result.json) |
| [20261029-024026-s8_fix_loop-deepseek-v4-baseline-rep5](20261029-024026-s8_fix_loop-deepseek-v4-baseline-rep5/) | s8_fix_loop | deepseek-v4-baseline | green | 228.6 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024026-s8_fix_loop-deepseek-v4-baseline-rep5/metrics.json) · [result](20261029-024026-s8_fix_loop-deepseek-v4-baseline-rep5/result.json) |
| [20261029-024154-s8_fix_loop-deepseek-v4-baseline-rep6](20261029-024154-s8_fix_loop-deepseek-v4-baseline-rep6/) | s8_fix_loop | deepseek-v4-baseline | green | 189.5 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024154-s8_fix_loop-deepseek-v4-baseline-rep6/metrics.json) · [result](20261029-024154-s8_fix_loop-deepseek-v4-baseline-rep6/result.json) |
| [20261029-024205-s8_fix_loop-deepseek-v4-baseline-rep7](20261029-024205-s8_fix_loop-deepseek-v4-baseline-rep7/) | s8_fix_loop | deepseek-v4-baseline | green | 93.4 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024205-s8_fix_loop-deepseek-v4-baseline-rep7/metrics.json) · [result](20261029-024205-s8_fix_loop-deepseek-v4-baseline-rep7/result.json) |
| [20261029-024346-s8_fix_loop-deepseek-v4-baseline-rep8](20261029-024346-s8_fix_loop-deepseek-v4-baseline-rep8/) | s8_fix_loop | deepseek-v4-baseline | green | 124.4 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024346-s8_fix_loop-deepseek-v4-baseline-rep8/metrics.json) · [result](20261029-024346-s8_fix_loop-deepseek-v4-baseline-rep8/result.json) |
| [20261029-024422-s8_fix_loop-deepseek-v4-baseline-rep9](20261029-024422-s8_fix_loop-deepseek-v4-baseline-rep9/) | s8_fix_loop | deepseek-v4-baseline | green | 105.4 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024422-s8_fix_loop-deepseek-v4-baseline-rep9/metrics.json) · [result](20261029-024422-s8_fix_loop-deepseek-v4-baseline-rep9/result.json) |
| [20261029-023536-s8_fix_loop-glm-5.3-baseline-rep0](20261029-023536-s8_fix_loop-glm-5.3-baseline-rep0/) | s8_fix_loop | glm-5.3-baseline | green | 28.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023536-s8_fix_loop-glm-5.3-baseline-rep0/metrics.json) · [result](20261029-023536-s8_fix_loop-glm-5.3-baseline-rep0/result.json) |
| [20261029-023538-s8_fix_loop-glm-5.3-baseline-rep1](20261029-023538-s8_fix_loop-glm-5.3-baseline-rep1/) | s8_fix_loop | glm-5.3-baseline | green | 30.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023538-s8_fix_loop-glm-5.3-baseline-rep1/metrics.json) · [result](20261029-023538-s8_fix_loop-glm-5.3-baseline-rep1/result.json) |
| [20261029-023614-s8_fix_loop-glm-5.3-baseline-rep2](20261029-023614-s8_fix_loop-glm-5.3-baseline-rep2/) | s8_fix_loop | glm-5.3-baseline | green | 30.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023614-s8_fix_loop-glm-5.3-baseline-rep2/metrics.json) · [result](20261029-023614-s8_fix_loop-glm-5.3-baseline-rep2/result.json) |
| [20261029-023614-s8_fix_loop-glm-5.3-baseline-rep3](20261029-023614-s8_fix_loop-glm-5.3-baseline-rep3/) | s8_fix_loop | glm-5.3-baseline | green | 34.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023614-s8_fix_loop-glm-5.3-baseline-rep3/metrics.json) · [result](20261029-023614-s8_fix_loop-glm-5.3-baseline-rep3/result.json) |
| [20261029-023617-s8_fix_loop-glm-5.3-baseline-rep4](20261029-023617-s8_fix_loop-glm-5.3-baseline-rep4/) | s8_fix_loop | glm-5.3-baseline | green | 29.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023617-s8_fix_loop-glm-5.3-baseline-rep4/metrics.json) · [result](20261029-023617-s8_fix_loop-glm-5.3-baseline-rep4/result.json) |
| [20261029-023651-s8_fix_loop-glm-5.3-baseline-rep5](20261029-023651-s8_fix_loop-glm-5.3-baseline-rep5/) | s8_fix_loop | glm-5.3-baseline | green | 30.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023651-s8_fix_loop-glm-5.3-baseline-rep5/metrics.json) · [result](20261029-023651-s8_fix_loop-glm-5.3-baseline-rep5/result.json) |
| [20261029-023652-s8_fix_loop-glm-5.3-baseline-rep6](20261029-023652-s8_fix_loop-glm-5.3-baseline-rep6/) | s8_fix_loop | glm-5.3-baseline | green | 35.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023652-s8_fix_loop-glm-5.3-baseline-rep6/metrics.json) · [result](20261029-023652-s8_fix_loop-glm-5.3-baseline-rep6/result.json) |
| [20261029-023655-s8_fix_loop-glm-5.3-baseline-rep7](20261029-023655-s8_fix_loop-glm-5.3-baseline-rep7/) | s8_fix_loop | glm-5.3-baseline | green | 40.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023655-s8_fix_loop-glm-5.3-baseline-rep7/metrics.json) · [result](20261029-023655-s8_fix_loop-glm-5.3-baseline-rep7/result.json) |
| [20261029-023734-s8_fix_loop-glm-5.3-baseline-rep8](20261029-023734-s8_fix_loop-glm-5.3-baseline-rep8/) | s8_fix_loop | glm-5.3-baseline | green | 25.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023734-s8_fix_loop-glm-5.3-baseline-rep8/metrics.json) · [result](20261029-023734-s8_fix_loop-glm-5.3-baseline-rep8/result.json) |
| [20261029-023739-s8_fix_loop-glm-5.3-baseline-rep9](20261029-023739-s8_fix_loop-glm-5.3-baseline-rep9/) | s8_fix_loop | glm-5.3-baseline | green | 25.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-023739-s8_fix_loop-glm-5.3-baseline-rep9/metrics.json) · [result](20261029-023739-s8_fix_loop-glm-5.3-baseline-rep9/result.json) |
| [20261029-024513-s8_fix_loop-incredible-four-rep0](20261029-024513-s8_fix_loop-incredible-four-rep0/) | s8_fix_loop | incredible-four | green | 60.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024513-s8_fix_loop-incredible-four-rep0/metrics.json) · [result](20261029-024513-s8_fix_loop-incredible-four-rep0/result.json) |
| [20261029-024601-s8_fix_loop-incredible-four-rep1](20261029-024601-s8_fix_loop-incredible-four-rep1/) | s8_fix_loop | incredible-four | green | 57.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024601-s8_fix_loop-incredible-four-rep1/metrics.json) · [result](20261029-024601-s8_fix_loop-incredible-four-rep1/result.json) |
| [20261029-024614-s8_fix_loop-incredible-four-rep2](20261029-024614-s8_fix_loop-incredible-four-rep2/) | s8_fix_loop | incredible-four | failed | 40.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024614-s8_fix_loop-incredible-four-rep2/metrics.json) · [result](20261029-024614-s8_fix_loop-incredible-four-rep2/result.json) |
| [20261029-024626-s8_fix_loop-incredible-four-rep3](20261029-024626-s8_fix_loop-incredible-four-rep3/) | s8_fix_loop | incredible-four | green | 62.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024626-s8_fix_loop-incredible-four-rep3/metrics.json) · [result](20261029-024626-s8_fix_loop-incredible-four-rep3/result.json) |
| [20261029-024703-s8_fix_loop-incredible-four-rep4](20261029-024703-s8_fix_loop-incredible-four-rep4/) | s8_fix_loop | incredible-four | green | 56.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024703-s8_fix_loop-incredible-four-rep4/metrics.json) · [result](20261029-024703-s8_fix_loop-incredible-four-rep4/result.json) |
| [20261029-024704-s8_fix_loop-incredible-four-rep5](20261029-024704-s8_fix_loop-incredible-four-rep5/) | s8_fix_loop | incredible-four | green | 108.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024704-s8_fix_loop-incredible-four-rep5/metrics.json) · [result](20261029-024704-s8_fix_loop-incredible-four-rep5/result.json) |
| [20261029-024737-s8_fix_loop-incredible-four-rep6](20261029-024737-s8_fix_loop-incredible-four-rep6/) | s8_fix_loop | incredible-four | green | 62.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024737-s8_fix_loop-incredible-four-rep6/metrics.json) · [result](20261029-024737-s8_fix_loop-incredible-four-rep6/result.json) |
| [20261029-024805-s8_fix_loop-incredible-four-rep7](20261029-024805-s8_fix_loop-incredible-four-rep7/) | s8_fix_loop | incredible-four | green | 73.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024805-s8_fix_loop-incredible-four-rep7/metrics.json) · [result](20261029-024805-s8_fix_loop-incredible-four-rep7/result.json) |
| [20261029-024851-s8_fix_loop-incredible-four-rep8](20261029-024851-s8_fix_loop-incredible-four-rep8/) | s8_fix_loop | incredible-four | green | 61.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024851-s8_fix_loop-incredible-four-rep8/metrics.json) · [result](20261029-024851-s8_fix_loop-incredible-four-rep8/result.json) |
| [20261029-024859-s8_fix_loop-incredible-four-rep9](20261029-024859-s8_fix_loop-incredible-four-rep9/) | s8_fix_loop | incredible-four | green | 62.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024859-s8_fix_loop-incredible-four-rep9/metrics.json) · [result](20261029-024859-s8_fix_loop-incredible-four-rep9/result.json) |
| [20261029-024925-s8_fix_loop-regular-three-rep0](20261029-024925-s8_fix_loop-regular-three-rep0/) | s8_fix_loop | regular-three | green | 25.3 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024925-s8_fix_loop-regular-three-rep0/metrics.json) · [result](20261029-024925-s8_fix_loop-regular-three-rep0/result.json) |
| [20261029-024957-s8_fix_loop-regular-three-rep1](20261029-024957-s8_fix_loop-regular-three-rep1/) | s8_fix_loop | regular-three | green | 27.2 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-024957-s8_fix_loop-regular-three-rep1/metrics.json) · [result](20261029-024957-s8_fix_loop-regular-three-rep1/result.json) |
| [20261029-025003-s8_fix_loop-regular-three-rep2](20261029-025003-s8_fix_loop-regular-three-rep2/) | s8_fix_loop | regular-three | green | 26.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-025003-s8_fix_loop-regular-three-rep2/metrics.json) · [result](20261029-025003-s8_fix_loop-regular-three-rep2/result.json) |
| [20261029-025008-s8_fix_loop-regular-three-rep3](20261029-025008-s8_fix_loop-regular-three-rep3/) | s8_fix_loop | regular-three | green | 24.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-025008-s8_fix_loop-regular-three-rep3/metrics.json) · [result](20261029-025008-s8_fix_loop-regular-three-rep3/result.json) |
| [20261029-025036-s8_fix_loop-regular-three-rep4](20261029-025036-s8_fix_loop-regular-three-rep4/) | s8_fix_loop | regular-three | green | 27.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-025036-s8_fix_loop-regular-three-rep4/metrics.json) · [result](20261029-025036-s8_fix_loop-regular-three-rep4/result.json) |
| [20261029-025036-s8_fix_loop-regular-three-rep5](20261029-025036-s8_fix_loop-regular-three-rep5/) | s8_fix_loop | regular-three | green | 42.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-025036-s8_fix_loop-regular-three-rep5/metrics.json) · [result](20261029-025036-s8_fix_loop-regular-three-rep5/result.json) |
| [20261029-025038-s8_fix_loop-regular-three-rep6](20261029-025038-s8_fix_loop-regular-three-rep6/) | s8_fix_loop | regular-three | green | 25.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-025038-s8_fix_loop-regular-three-rep6/metrics.json) · [result](20261029-025038-s8_fix_loop-regular-three-rep6/result.json) |
| [20261029-025110-s8_fix_loop-regular-three-rep7](20261029-025110-s8_fix_loop-regular-three-rep7/) | s8_fix_loop | regular-three | green | 28.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-025110-s8_fix_loop-regular-three-rep7/metrics.json) · [result](20261029-025110-s8_fix_loop-regular-three-rep7/result.json) |
| [20261029-025110-s8_fix_loop-regular-three-rep8](20261029-025110-s8_fix_loop-regular-three-rep8/) | s8_fix_loop | regular-three | green | 26.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-025110-s8_fix_loop-regular-three-rep8/metrics.json) · [result](20261029-025110-s8_fix_loop-regular-three-rep8/result.json) |
| [20261029-025125-s8_fix_loop-regular-three-rep9](20261029-025125-s8_fix_loop-regular-three-rep9/) | s8_fix_loop | regular-three | green | 25.1 s | — | 0/0/0 | 2 | 0 | feature:Verified successfully | ok | clean | [metrics](20261029-025125-s8_fix_loop-regular-three-rep9/metrics.json) · [result](20261029-025125-s8_fix_loop-regular-three-rep9/result.json) |
| [20261029-025219-s9_research_count-deepseek-v4-baseline-rep0](20261029-025219-s9_research_count-deepseek-v4-baseline-rep0/) | s9_research_count | deepseek-v4-baseline | green | 13.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025219-s9_research_count-deepseek-v4-baseline-rep0/metrics.json) · [result](20261029-025219-s9_research_count-deepseek-v4-baseline-rep0/result.json) |
| [20261029-025229-s9_research_count-deepseek-v4-baseline-rep1](20261029-025229-s9_research_count-deepseek-v4-baseline-rep1/) | s9_research_count | deepseek-v4-baseline | green | 17.1 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025229-s9_research_count-deepseek-v4-baseline-rep1/metrics.json) · [result](20261029-025229-s9_research_count-deepseek-v4-baseline-rep1/result.json) |
| [20261029-025230-s9_research_count-deepseek-v4-baseline-rep2](20261029-025230-s9_research_count-deepseek-v4-baseline-rep2/) | s9_research_count | deepseek-v4-baseline | green | 20.1 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025230-s9_research_count-deepseek-v4-baseline-rep2/metrics.json) · [result](20261029-025230-s9_research_count-deepseek-v4-baseline-rep2/result.json) |
| [20261029-025238-s9_research_count-deepseek-v4-baseline-rep3](20261029-025238-s9_research_count-deepseek-v4-baseline-rep3/) | s9_research_count | deepseek-v4-baseline | green | 15.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025238-s9_research_count-deepseek-v4-baseline-rep3/metrics.json) · [result](20261029-025238-s9_research_count-deepseek-v4-baseline-rep3/result.json) |
| [20261029-025251-s9_research_count-deepseek-v4-baseline-rep4](20261029-025251-s9_research_count-deepseek-v4-baseline-rep4/) | s9_research_count | deepseek-v4-baseline | green | 18.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025251-s9_research_count-deepseek-v4-baseline-rep4/metrics.json) · [result](20261029-025251-s9_research_count-deepseek-v4-baseline-rep4/result.json) |
| [20261029-025255-s9_research_count-deepseek-v4-baseline-rep5](20261029-025255-s9_research_count-deepseek-v4-baseline-rep5/) | s9_research_count | deepseek-v4-baseline | green | 20.1 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025255-s9_research_count-deepseek-v4-baseline-rep5/metrics.json) · [result](20261029-025255-s9_research_count-deepseek-v4-baseline-rep5/result.json) |
| [20261029-025258-s9_research_count-deepseek-v4-baseline-rep6](20261029-025258-s9_research_count-deepseek-v4-baseline-rep6/) | s9_research_count | deepseek-v4-baseline | green | 12.1 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025258-s9_research_count-deepseek-v4-baseline-rep6/metrics.json) · [result](20261029-025258-s9_research_count-deepseek-v4-baseline-rep6/result.json) |
| [20261029-025315-s9_research_count-deepseek-v4-baseline-rep7](20261029-025315-s9_research_count-deepseek-v4-baseline-rep7/) | s9_research_count | deepseek-v4-baseline | green | 14.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025315-s9_research_count-deepseek-v4-baseline-rep7/metrics.json) · [result](20261029-025315-s9_research_count-deepseek-v4-baseline-rep7/result.json) |
| [20261029-025315-s9_research_count-deepseek-v4-baseline-rep8](20261029-025315-s9_research_count-deepseek-v4-baseline-rep8/) | s9_research_count | deepseek-v4-baseline | green | 11.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025315-s9_research_count-deepseek-v4-baseline-rep8/metrics.json) · [result](20261029-025315-s9_research_count-deepseek-v4-baseline-rep8/result.json) |
| [20261029-025320-s9_research_count-deepseek-v4-baseline-rep9](20261029-025320-s9_research_count-deepseek-v4-baseline-rep9/) | s9_research_count | deepseek-v4-baseline | green | 20.2 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025320-s9_research_count-deepseek-v4-baseline-rep9/metrics.json) · [result](20261029-025320-s9_research_count-deepseek-v4-baseline-rep9/result.json) |
| [20261029-025147-s9_research_count-glm-5.3-baseline-rep0](20261029-025147-s9_research_count-glm-5.3-baseline-rep0/) | s9_research_count | glm-5.3-baseline | green | 3.1 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025147-s9_research_count-glm-5.3-baseline-rep0/metrics.json) · [result](20261029-025147-s9_research_count-glm-5.3-baseline-rep0/result.json) |
| [20261029-025149-s9_research_count-glm-5.3-baseline-rep1](20261029-025149-s9_research_count-glm-5.3-baseline-rep1/) | s9_research_count | glm-5.3-baseline | green | 4.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025149-s9_research_count-glm-5.3-baseline-rep1/metrics.json) · [result](20261029-025149-s9_research_count-glm-5.3-baseline-rep1/result.json) |
| [20261029-025155-s9_research_count-glm-5.3-baseline-rep2](20261029-025155-s9_research_count-glm-5.3-baseline-rep2/) | s9_research_count | glm-5.3-baseline | green | 7.2 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025155-s9_research_count-glm-5.3-baseline-rep2/metrics.json) · [result](20261029-025155-s9_research_count-glm-5.3-baseline-rep2/result.json) |
| [20261029-025157-s9_research_count-glm-5.3-baseline-rep3](20261029-025157-s9_research_count-glm-5.3-baseline-rep3/) | s9_research_count | glm-5.3-baseline | green | 7.1 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025157-s9_research_count-glm-5.3-baseline-rep3/metrics.json) · [result](20261029-025157-s9_research_count-glm-5.3-baseline-rep3/result.json) |
| [20261029-025158-s9_research_count-glm-5.3-baseline-rep4](20261029-025158-s9_research_count-glm-5.3-baseline-rep4/) | s9_research_count | glm-5.3-baseline | green | 4.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025158-s9_research_count-glm-5.3-baseline-rep4/metrics.json) · [result](20261029-025158-s9_research_count-glm-5.3-baseline-rep4/result.json) |
| [20261029-025207-s9_research_count-glm-5.3-baseline-rep5](20261029-025207-s9_research_count-glm-5.3-baseline-rep5/) | s9_research_count | glm-5.3-baseline | green | 4.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025207-s9_research_count-glm-5.3-baseline-rep5/metrics.json) · [result](20261029-025207-s9_research_count-glm-5.3-baseline-rep5/result.json) |
| [20261029-025208-s9_research_count-glm-5.3-baseline-rep6](20261029-025208-s9_research_count-glm-5.3-baseline-rep6/) | s9_research_count | glm-5.3-baseline | green | 3.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025208-s9_research_count-glm-5.3-baseline-rep6/metrics.json) · [result](20261029-025208-s9_research_count-glm-5.3-baseline-rep6/result.json) |
| [20261029-025210-s9_research_count-glm-5.3-baseline-rep7](20261029-025210-s9_research_count-glm-5.3-baseline-rep7/) | s9_research_count | glm-5.3-baseline | green | 4.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025210-s9_research_count-glm-5.3-baseline-rep7/metrics.json) · [result](20261029-025210-s9_research_count-glm-5.3-baseline-rep7/result.json) |
| [20261029-025216-s9_research_count-glm-5.3-baseline-rep8](20261029-025216-s9_research_count-glm-5.3-baseline-rep8/) | s9_research_count | glm-5.3-baseline | green | 5.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025216-s9_research_count-glm-5.3-baseline-rep8/metrics.json) · [result](20261029-025216-s9_research_count-glm-5.3-baseline-rep8/result.json) |
| [20261029-025216-s9_research_count-glm-5.3-baseline-rep9](20261029-025216-s9_research_count-glm-5.3-baseline-rep9/) | s9_research_count | glm-5.3-baseline | green | 4.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025216-s9_research_count-glm-5.3-baseline-rep9/metrics.json) · [result](20261029-025216-s9_research_count-glm-5.3-baseline-rep9/result.json) |
| [20261029-025331-s9_research_count-incredible-four-rep0](20261029-025331-s9_research_count-incredible-four-rep0/) | s9_research_count | incredible-four | green | 20.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025331-s9_research_count-incredible-four-rep0/metrics.json) · [result](20261029-025331-s9_research_count-incredible-four-rep0/result.json) |
| [20261029-025334-s9_research_count-incredible-four-rep1](20261029-025334-s9_research_count-incredible-four-rep1/) | s9_research_count | incredible-four | green | 12.1 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025334-s9_research_count-incredible-four-rep1/metrics.json) · [result](20261029-025334-s9_research_count-incredible-four-rep1/result.json) |
| [20261029-025349-s9_research_count-incredible-four-rep2](20261029-025349-s9_research_count-incredible-four-rep2/) | s9_research_count | incredible-four | green | 16.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025349-s9_research_count-incredible-four-rep2/metrics.json) · [result](20261029-025349-s9_research_count-incredible-four-rep2/result.json) |
| [20261029-025351-s9_research_count-incredible-four-rep3](20261029-025351-s9_research_count-incredible-four-rep3/) | s9_research_count | incredible-four | green | 17.1 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025351-s9_research_count-incredible-four-rep3/metrics.json) · [result](20261029-025351-s9_research_count-incredible-four-rep3/result.json) |
| [20261029-025356-s9_research_count-incredible-four-rep4](20261029-025356-s9_research_count-incredible-four-rep4/) | s9_research_count | incredible-four | green | 21.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025356-s9_research_count-incredible-four-rep4/metrics.json) · [result](20261029-025356-s9_research_count-incredible-four-rep4/result.json) |
| [20261029-025411-s9_research_count-incredible-four-rep5](20261029-025411-s9_research_count-incredible-four-rep5/) | s9_research_count | incredible-four | green | 17.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025411-s9_research_count-incredible-four-rep5/metrics.json) · [result](20261029-025411-s9_research_count-incredible-four-rep5/result.json) |
| [20261029-025413-s9_research_count-incredible-four-rep6](20261029-025413-s9_research_count-incredible-four-rep6/) | s9_research_count | incredible-four | green | 24.1 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025413-s9_research_count-incredible-four-rep6/metrics.json) · [result](20261029-025413-s9_research_count-incredible-four-rep6/result.json) |
| [20261029-025423-s9_research_count-incredible-four-rep7](20261029-025423-s9_research_count-incredible-four-rep7/) | s9_research_count | incredible-four | green | 14.1 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025423-s9_research_count-incredible-four-rep7/metrics.json) · [result](20261029-025423-s9_research_count-incredible-four-rep7/result.json) |
| [20261029-025433-s9_research_count-incredible-four-rep8](20261029-025433-s9_research_count-incredible-four-rep8/) | s9_research_count | incredible-four | green | 13.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025433-s9_research_count-incredible-four-rep8/metrics.json) · [result](20261029-025433-s9_research_count-incredible-four-rep8/result.json) |
| [20261029-025442-s9_research_count-incredible-four-rep9](20261029-025442-s9_research_count-incredible-four-rep9/) | s9_research_count | incredible-four | green | 21.3 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025442-s9_research_count-incredible-four-rep9/metrics.json) · [result](20261029-025442-s9_research_count-incredible-four-rep9/result.json) |
| [20261029-025446-s9_research_count-regular-three-rep0](20261029-025446-s9_research_count-regular-three-rep0/) | s9_research_count | regular-three | green | 5.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025446-s9_research_count-regular-three-rep0/metrics.json) · [result](20261029-025446-s9_research_count-regular-three-rep0/result.json) |
| [20261029-025451-s9_research_count-regular-three-rep1](20261029-025451-s9_research_count-regular-three-rep1/) | s9_research_count | regular-three | green | 10.1 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025451-s9_research_count-regular-three-rep1/metrics.json) · [result](20261029-025451-s9_research_count-regular-three-rep1/result.json) |
| [20261029-025456-s9_research_count-regular-three-rep2](20261029-025456-s9_research_count-regular-three-rep2/) | s9_research_count | regular-three | green | 6.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025456-s9_research_count-regular-three-rep2/metrics.json) · [result](20261029-025456-s9_research_count-regular-three-rep2/result.json) |
| [20261029-025507-s9_research_count-regular-three-rep3](20261029-025507-s9_research_count-regular-three-rep3/) | s9_research_count | regular-three | green | 11.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025507-s9_research_count-regular-three-rep3/metrics.json) · [result](20261029-025507-s9_research_count-regular-three-rep3/result.json) |
| [20261029-025507-s9_research_count-regular-three-rep4](20261029-025507-s9_research_count-regular-three-rep4/) | s9_research_count | regular-three | green | 9.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025507-s9_research_count-regular-three-rep4/metrics.json) · [result](20261029-025507-s9_research_count-regular-three-rep4/result.json) |
| [20261029-025508-s9_research_count-regular-three-rep5](20261029-025508-s9_research_count-regular-three-rep5/) | s9_research_count | regular-three | green | 11.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025508-s9_research_count-regular-three-rep5/metrics.json) · [result](20261029-025508-s9_research_count-regular-three-rep5/result.json) |
| [20261029-025521-s9_research_count-regular-three-rep6](20261029-025521-s9_research_count-regular-three-rep6/) | s9_research_count | regular-three | green | 4.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025521-s9_research_count-regular-three-rep6/metrics.json) · [result](20261029-025521-s9_research_count-regular-three-rep6/result.json) |
| [20261029-025523-s9_research_count-regular-three-rep7](20261029-025523-s9_research_count-regular-three-rep7/) | s9_research_count | regular-three | green | 5.1 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025523-s9_research_count-regular-three-rep7/metrics.json) · [result](20261029-025523-s9_research_count-regular-three-rep7/result.json) |
| [20261029-025524-s9_research_count-regular-three-rep8](20261029-025524-s9_research_count-regular-three-rep8/) | s9_research_count | regular-three | green | 5.0 s | no | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025524-s9_research_count-regular-three-rep8/metrics.json) · [result](20261029-025524-s9_research_count-regular-three-rep8/result.json) |
| [20261029-025531-s9_research_count-regular-three-rep9](20261029-025531-s9_research_count-regular-three-rep9/) | s9_research_count | regular-three | green | 5.0 s | yes | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261029-025531-s9_research_count-regular-three-rep9/metrics.json) · [result](20261029-025531-s9_research_count-regular-three-rep9/result.json) |
| [20261028-225813-s10_research_facts-deepseek-v4-baseline-rep0](20261028-225813-s10_research_facts-deepseek-v4-baseline-rep0/) | s10_research_facts | deepseek-v4-baseline | green | 51.3 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225813-s10_research_facts-deepseek-v4-baseline-rep0/metrics.json) · [result](20261028-225813-s10_research_facts-deepseek-v4-baseline-rep0/result.json) |
| [20261028-225817-s10_research_facts-deepseek-v4-baseline-rep1](20261028-225817-s10_research_facts-deepseek-v4-baseline-rep1/) | s10_research_facts | deepseek-v4-baseline | green | 57.2 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225817-s10_research_facts-deepseek-v4-baseline-rep1/metrics.json) · [result](20261028-225817-s10_research_facts-deepseek-v4-baseline-rep1/result.json) |
| [20261028-225826-s10_research_facts-deepseek-v4-baseline-rep2](20261028-225826-s10_research_facts-deepseek-v4-baseline-rep2/) | s10_research_facts | deepseek-v4-baseline | green | 55.2 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225826-s10_research_facts-deepseek-v4-baseline-rep2/metrics.json) · [result](20261028-225826-s10_research_facts-deepseek-v4-baseline-rep2/result.json) |
| [20261028-225909-s10_research_facts-deepseek-v4-baseline-rep3](20261028-225909-s10_research_facts-deepseek-v4-baseline-rep3/) | s10_research_facts | deepseek-v4-baseline | green | 52.2 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225909-s10_research_facts-deepseek-v4-baseline-rep3/metrics.json) · [result](20261028-225909-s10_research_facts-deepseek-v4-baseline-rep3/result.json) |
| [20261028-225919-s10_research_facts-deepseek-v4-baseline-rep4](20261028-225919-s10_research_facts-deepseek-v4-baseline-rep4/) | s10_research_facts | deepseek-v4-baseline | green | 54.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225919-s10_research_facts-deepseek-v4-baseline-rep4/metrics.json) · [result](20261028-225919-s10_research_facts-deepseek-v4-baseline-rep4/result.json) |
| [20261028-225931-s10_research_facts-deepseek-v4-baseline-rep5](20261028-225931-s10_research_facts-deepseek-v4-baseline-rep5/) | s10_research_facts | deepseek-v4-baseline | green | 61.2 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225931-s10_research_facts-deepseek-v4-baseline-rep5/metrics.json) · [result](20261028-225931-s10_research_facts-deepseek-v4-baseline-rep5/result.json) |
| [20261028-230006-s10_research_facts-deepseek-v4-baseline-rep6](20261028-230006-s10_research_facts-deepseek-v4-baseline-rep6/) | s10_research_facts | deepseek-v4-baseline | green | 60.2 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230006-s10_research_facts-deepseek-v4-baseline-rep6/metrics.json) · [result](20261028-230006-s10_research_facts-deepseek-v4-baseline-rep6/result.json) |
| [20261028-230017-s10_research_facts-deepseek-v4-baseline-rep7](20261028-230017-s10_research_facts-deepseek-v4-baseline-rep7/) | s10_research_facts | deepseek-v4-baseline | green | 57.2 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230017-s10_research_facts-deepseek-v4-baseline-rep7/metrics.json) · [result](20261028-230017-s10_research_facts-deepseek-v4-baseline-rep7/result.json) |
| [20261028-230043-s10_research_facts-deepseek-v4-baseline-rep8](20261028-230043-s10_research_facts-deepseek-v4-baseline-rep8/) | s10_research_facts | deepseek-v4-baseline | green | 59.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230043-s10_research_facts-deepseek-v4-baseline-rep8/metrics.json) · [result](20261028-230043-s10_research_facts-deepseek-v4-baseline-rep8/result.json) |
| [20261028-230112-s10_research_facts-deepseek-v4-baseline-rep9](20261028-230112-s10_research_facts-deepseek-v4-baseline-rep9/) | s10_research_facts | deepseek-v4-baseline | green | 45.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230112-s10_research_facts-deepseek-v4-baseline-rep9/metrics.json) · [result](20261028-230112-s10_research_facts-deepseek-v4-baseline-rep9/result.json) |
| [20261028-225725-s10_research_facts-glm-5.3-baseline-rep0](20261028-225725-s10_research_facts-glm-5.3-baseline-rep0/) | s10_research_facts | glm-5.3-baseline | green | 13.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225725-s10_research_facts-glm-5.3-baseline-rep0/metrics.json) · [result](20261028-225725-s10_research_facts-glm-5.3-baseline-rep0/result.json) |
| [20261028-225725-s10_research_facts-glm-5.3-baseline-rep1](20261028-225725-s10_research_facts-glm-5.3-baseline-rep1/) | s10_research_facts | glm-5.3-baseline | green | 8.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225725-s10_research_facts-glm-5.3-baseline-rep1/metrics.json) · [result](20261028-225725-s10_research_facts-glm-5.3-baseline-rep1/result.json) |
| [20261028-225725-s10_research_facts-glm-5.3-baseline-rep2](20261028-225725-s10_research_facts-glm-5.3-baseline-rep2/) | s10_research_facts | glm-5.3-baseline | green | 12.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225725-s10_research_facts-glm-5.3-baseline-rep2/metrics.json) · [result](20261028-225725-s10_research_facts-glm-5.3-baseline-rep2/result.json) |
| [20261028-225741-s10_research_facts-glm-5.3-baseline-rep3](20261028-225741-s10_research_facts-glm-5.3-baseline-rep3/) | s10_research_facts | glm-5.3-baseline | green | 10.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225741-s10_research_facts-glm-5.3-baseline-rep3/metrics.json) · [result](20261028-225741-s10_research_facts-glm-5.3-baseline-rep3/result.json) |
| [20261028-225745-s10_research_facts-glm-5.3-baseline-rep4](20261028-225745-s10_research_facts-glm-5.3-baseline-rep4/) | s10_research_facts | glm-5.3-baseline | green | 9.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225745-s10_research_facts-glm-5.3-baseline-rep4/metrics.json) · [result](20261028-225745-s10_research_facts-glm-5.3-baseline-rep4/result.json) |
| [20261028-225746-s10_research_facts-glm-5.3-baseline-rep5](20261028-225746-s10_research_facts-glm-5.3-baseline-rep5/) | s10_research_facts | glm-5.3-baseline | green | 9.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225746-s10_research_facts-glm-5.3-baseline-rep5/metrics.json) · [result](20261028-225746-s10_research_facts-glm-5.3-baseline-rep5/result.json) |
| [20261028-225756-s10_research_facts-glm-5.3-baseline-rep6](20261028-225756-s10_research_facts-glm-5.3-baseline-rep6/) | s10_research_facts | glm-5.3-baseline | green | 9.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225756-s10_research_facts-glm-5.3-baseline-rep6/metrics.json) · [result](20261028-225756-s10_research_facts-glm-5.3-baseline-rep6/result.json) |
| [20261028-225759-s10_research_facts-glm-5.3-baseline-rep7](20261028-225759-s10_research_facts-glm-5.3-baseline-rep7/) | s10_research_facts | glm-5.3-baseline | failed | 9.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225759-s10_research_facts-glm-5.3-baseline-rep7/metrics.json) · [result](20261028-225759-s10_research_facts-glm-5.3-baseline-rep7/result.json) |
| [20261028-225800-s10_research_facts-glm-5.3-baseline-rep8](20261028-225800-s10_research_facts-glm-5.3-baseline-rep8/) | s10_research_facts | glm-5.3-baseline | green | 12.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225800-s10_research_facts-glm-5.3-baseline-rep8/metrics.json) · [result](20261028-225800-s10_research_facts-glm-5.3-baseline-rep8/result.json) |
| [20261028-225810-s10_research_facts-glm-5.3-baseline-rep9](20261028-225810-s10_research_facts-glm-5.3-baseline-rep9/) | s10_research_facts | glm-5.3-baseline | green | 10.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-225810-s10_research_facts-glm-5.3-baseline-rep9/metrics.json) · [result](20261028-225810-s10_research_facts-glm-5.3-baseline-rep9/result.json) |
| [20261028-230119-s10_research_facts-incredible-four-rep0](20261028-230119-s10_research_facts-incredible-four-rep0/) | s10_research_facts | incredible-four | green | 59.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230119-s10_research_facts-incredible-four-rep0/metrics.json) · [result](20261028-230119-s10_research_facts-incredible-four-rep0/result.json) |
| [20261028-230152-s10_research_facts-incredible-four-rep1](20261028-230152-s10_research_facts-incredible-four-rep1/) | s10_research_facts | incredible-four | green | 41.2 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230152-s10_research_facts-incredible-four-rep1/metrics.json) · [result](20261028-230152-s10_research_facts-incredible-four-rep1/result.json) |
| [20261028-230202-s10_research_facts-incredible-four-rep2](20261028-230202-s10_research_facts-incredible-four-rep2/) | s10_research_facts | incredible-four | green | 49.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230202-s10_research_facts-incredible-four-rep2/metrics.json) · [result](20261028-230202-s10_research_facts-incredible-four-rep2/result.json) |
| [20261028-230223-s10_research_facts-incredible-four-rep3](20261028-230223-s10_research_facts-incredible-four-rep3/) | s10_research_facts | incredible-four | green | 49.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230223-s10_research_facts-incredible-four-rep3/metrics.json) · [result](20261028-230223-s10_research_facts-incredible-four-rep3/result.json) |
| [20261028-230243-s10_research_facts-incredible-four-rep4](20261028-230243-s10_research_facts-incredible-four-rep4/) | s10_research_facts | incredible-four | green | 49.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230243-s10_research_facts-incredible-four-rep4/metrics.json) · [result](20261028-230243-s10_research_facts-incredible-four-rep4/result.json) |
| [20261028-230255-s10_research_facts-incredible-four-rep5](20261028-230255-s10_research_facts-incredible-four-rep5/) | s10_research_facts | incredible-four | green | 46.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230255-s10_research_facts-incredible-four-rep5/metrics.json) · [result](20261028-230255-s10_research_facts-incredible-four-rep5/result.json) |
| [20261028-230317-s10_research_facts-incredible-four-rep6](20261028-230317-s10_research_facts-incredible-four-rep6/) | s10_research_facts | incredible-four | green | 54.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230317-s10_research_facts-incredible-four-rep6/metrics.json) · [result](20261028-230317-s10_research_facts-incredible-four-rep6/result.json) |
| [20261028-230337-s10_research_facts-incredible-four-rep7](20261028-230337-s10_research_facts-incredible-four-rep7/) | s10_research_facts | incredible-four | green | 45.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230337-s10_research_facts-incredible-four-rep7/metrics.json) · [result](20261028-230337-s10_research_facts-incredible-four-rep7/result.json) |
| [20261028-230351-s10_research_facts-incredible-four-rep8](20261028-230351-s10_research_facts-incredible-four-rep8/) | s10_research_facts | incredible-four | green | 43.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230351-s10_research_facts-incredible-four-rep8/metrics.json) · [result](20261028-230351-s10_research_facts-incredible-four-rep8/result.json) |
| [20261028-230416-s10_research_facts-incredible-four-rep9](20261028-230416-s10_research_facts-incredible-four-rep9/) | s10_research_facts | incredible-four | green | 40.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230416-s10_research_facts-incredible-four-rep9/metrics.json) · [result](20261028-230416-s10_research_facts-incredible-four-rep9/result.json) |
| [20261028-230427-s10_research_facts-regular-three-rep0](20261028-230427-s10_research_facts-regular-three-rep0/) | s10_research_facts | regular-three | green | 10.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230427-s10_research_facts-regular-three-rep0/metrics.json) · [result](20261028-230427-s10_research_facts-regular-three-rep0/result.json) |
| [20261028-230439-s10_research_facts-regular-three-rep1](20261028-230439-s10_research_facts-regular-three-rep1/) | s10_research_facts | regular-three | green | 9.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230439-s10_research_facts-regular-three-rep1/metrics.json) · [result](20261028-230439-s10_research_facts-regular-three-rep1/result.json) |
| [20261028-230441-s10_research_facts-regular-three-rep2](20261028-230441-s10_research_facts-regular-three-rep2/) | s10_research_facts | regular-three | green | 16.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230441-s10_research_facts-regular-three-rep2/metrics.json) · [result](20261028-230441-s10_research_facts-regular-three-rep2/result.json) |
| [20261028-230453-s10_research_facts-regular-three-rep3](20261028-230453-s10_research_facts-regular-three-rep3/) | s10_research_facts | regular-three | green | 9.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230453-s10_research_facts-regular-three-rep3/metrics.json) · [result](20261028-230453-s10_research_facts-regular-three-rep3/result.json) |
| [20261028-230502-s10_research_facts-regular-three-rep4](20261028-230502-s10_research_facts-regular-three-rep4/) | s10_research_facts | regular-three | green | 10.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230502-s10_research_facts-regular-three-rep4/metrics.json) · [result](20261028-230502-s10_research_facts-regular-three-rep4/result.json) |
| [20261028-230506-s10_research_facts-regular-three-rep5](20261028-230506-s10_research_facts-regular-three-rep5/) | s10_research_facts | regular-three | green | 11.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230506-s10_research_facts-regular-three-rep5/metrics.json) · [result](20261028-230506-s10_research_facts-regular-three-rep5/result.json) |
| [20261028-230506-s10_research_facts-regular-three-rep6](20261028-230506-s10_research_facts-regular-three-rep6/) | s10_research_facts | regular-three | green | 10.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230506-s10_research_facts-regular-three-rep6/metrics.json) · [result](20261028-230506-s10_research_facts-regular-three-rep6/result.json) |
| [20261028-230517-s10_research_facts-regular-three-rep7](20261028-230517-s10_research_facts-regular-three-rep7/) | s10_research_facts | regular-three | green | 12.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230517-s10_research_facts-regular-three-rep7/metrics.json) · [result](20261028-230517-s10_research_facts-regular-three-rep7/result.json) |
| [20261028-230521-s10_research_facts-regular-three-rep8](20261028-230521-s10_research_facts-regular-three-rep8/) | s10_research_facts | regular-three | green | 11.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230521-s10_research_facts-regular-three-rep8/metrics.json) · [result](20261028-230521-s10_research_facts-regular-three-rep8/result.json) |
| [20261028-230522-s10_research_facts-regular-three-rep9](20261028-230522-s10_research_facts-regular-three-rep9/) | s10_research_facts | regular-three | green | 12.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230522-s10_research_facts-regular-three-rep9/metrics.json) · [result](20261028-230522-s10_research_facts-regular-three-rep9/result.json) |
| [20261028-230620-s11_research_routes-deepseek-v4-baseline-rep0](20261028-230620-s11_research_routes-deepseek-v4-baseline-rep0/) | s11_research_routes | deepseek-v4-baseline | green | 28.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230620-s11_research_routes-deepseek-v4-baseline-rep0/metrics.json) · [result](20261028-230620-s11_research_routes-deepseek-v4-baseline-rep0/result.json) |
| [20261028-230622-s11_research_routes-deepseek-v4-baseline-rep1](20261028-230622-s11_research_routes-deepseek-v4-baseline-rep1/) | s11_research_routes | deepseek-v4-baseline | green | 20.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230622-s11_research_routes-deepseek-v4-baseline-rep1/metrics.json) · [result](20261028-230622-s11_research_routes-deepseek-v4-baseline-rep1/result.json) |
| [20261028-230623-s11_research_routes-deepseek-v4-baseline-rep2](20261028-230623-s11_research_routes-deepseek-v4-baseline-rep2/) | s11_research_routes | deepseek-v4-baseline | green | 30.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230623-s11_research_routes-deepseek-v4-baseline-rep2/metrics.json) · [result](20261028-230623-s11_research_routes-deepseek-v4-baseline-rep2/result.json) |
| [20261028-230648-s11_research_routes-deepseek-v4-baseline-rep3](20261028-230648-s11_research_routes-deepseek-v4-baseline-rep3/) | s11_research_routes | deepseek-v4-baseline | green | 25.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230648-s11_research_routes-deepseek-v4-baseline-rep3/metrics.json) · [result](20261028-230648-s11_research_routes-deepseek-v4-baseline-rep3/result.json) |
| [20261028-230655-s11_research_routes-deepseek-v4-baseline-rep4](20261028-230655-s11_research_routes-deepseek-v4-baseline-rep4/) | s11_research_routes | deepseek-v4-baseline | green | 22.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230655-s11_research_routes-deepseek-v4-baseline-rep4/metrics.json) · [result](20261028-230655-s11_research_routes-deepseek-v4-baseline-rep4/result.json) |
| [20261028-230704-s11_research_routes-deepseek-v4-baseline-rep5](20261028-230704-s11_research_routes-deepseek-v4-baseline-rep5/) | s11_research_routes | deepseek-v4-baseline | green | 20.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230704-s11_research_routes-deepseek-v4-baseline-rep5/metrics.json) · [result](20261028-230704-s11_research_routes-deepseek-v4-baseline-rep5/result.json) |
| [20261028-230718-s11_research_routes-deepseek-v4-baseline-rep6](20261028-230718-s11_research_routes-deepseek-v4-baseline-rep6/) | s11_research_routes | deepseek-v4-baseline | green | 18.2 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230718-s11_research_routes-deepseek-v4-baseline-rep6/metrics.json) · [result](20261028-230718-s11_research_routes-deepseek-v4-baseline-rep6/result.json) |
| [20261028-230722-s11_research_routes-deepseek-v4-baseline-rep7](20261028-230722-s11_research_routes-deepseek-v4-baseline-rep7/) | s11_research_routes | deepseek-v4-baseline | green | 24.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230722-s11_research_routes-deepseek-v4-baseline-rep7/metrics.json) · [result](20261028-230722-s11_research_routes-deepseek-v4-baseline-rep7/result.json) |
| [20261028-230729-s11_research_routes-deepseek-v4-baseline-rep8](20261028-230729-s11_research_routes-deepseek-v4-baseline-rep8/) | s11_research_routes | deepseek-v4-baseline | green | 22.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230729-s11_research_routes-deepseek-v4-baseline-rep8/metrics.json) · [result](20261028-230729-s11_research_routes-deepseek-v4-baseline-rep8/result.json) |
| [20261028-230741-s11_research_routes-deepseek-v4-baseline-rep9](20261028-230741-s11_research_routes-deepseek-v4-baseline-rep9/) | s11_research_routes | deepseek-v4-baseline | green | 19.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230741-s11_research_routes-deepseek-v4-baseline-rep9/metrics.json) · [result](20261028-230741-s11_research_routes-deepseek-v4-baseline-rep9/result.json) |
| [20261028-230535-s11_research_routes-glm-5.3-baseline-rep0](20261028-230535-s11_research_routes-glm-5.3-baseline-rep0/) | s11_research_routes | glm-5.3-baseline | green | 10.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230535-s11_research_routes-glm-5.3-baseline-rep0/metrics.json) · [result](20261028-230535-s11_research_routes-glm-5.3-baseline-rep0/result.json) |
| [20261028-230542-s11_research_routes-glm-5.3-baseline-rep1](20261028-230542-s11_research_routes-glm-5.3-baseline-rep1/) | s11_research_routes | glm-5.3-baseline | green | 10.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230542-s11_research_routes-glm-5.3-baseline-rep1/metrics.json) · [result](20261028-230542-s11_research_routes-glm-5.3-baseline-rep1/result.json) |
| [20261028-230543-s11_research_routes-glm-5.3-baseline-rep2](20261028-230543-s11_research_routes-glm-5.3-baseline-rep2/) | s11_research_routes | glm-5.3-baseline | green | 11.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230543-s11_research_routes-glm-5.3-baseline-rep2/metrics.json) · [result](20261028-230543-s11_research_routes-glm-5.3-baseline-rep2/result.json) |
| [20261028-230550-s11_research_routes-glm-5.3-baseline-rep3](20261028-230550-s11_research_routes-glm-5.3-baseline-rep3/) | s11_research_routes | glm-5.3-baseline | green | 6.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230550-s11_research_routes-glm-5.3-baseline-rep3/metrics.json) · [result](20261028-230550-s11_research_routes-glm-5.3-baseline-rep3/result.json) |
| [20261028-230557-s11_research_routes-glm-5.3-baseline-rep4](20261028-230557-s11_research_routes-glm-5.3-baseline-rep4/) | s11_research_routes | glm-5.3-baseline | green | 5.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230557-s11_research_routes-glm-5.3-baseline-rep4/metrics.json) · [result](20261028-230557-s11_research_routes-glm-5.3-baseline-rep4/result.json) |
| [20261028-230600-s11_research_routes-glm-5.3-baseline-rep5](20261028-230600-s11_research_routes-glm-5.3-baseline-rep5/) | s11_research_routes | glm-5.3-baseline | green | 8.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230600-s11_research_routes-glm-5.3-baseline-rep5/metrics.json) · [result](20261028-230600-s11_research_routes-glm-5.3-baseline-rep5/result.json) |
| [20261028-230601-s11_research_routes-glm-5.3-baseline-rep6](20261028-230601-s11_research_routes-glm-5.3-baseline-rep6/) | s11_research_routes | glm-5.3-baseline | green | 5.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230601-s11_research_routes-glm-5.3-baseline-rep6/metrics.json) · [result](20261028-230601-s11_research_routes-glm-5.3-baseline-rep6/result.json) |
| [20261028-230608-s11_research_routes-glm-5.3-baseline-rep7](20261028-230608-s11_research_routes-glm-5.3-baseline-rep7/) | s11_research_routes | glm-5.3-baseline | green | 6.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230608-s11_research_routes-glm-5.3-baseline-rep7/metrics.json) · [result](20261028-230608-s11_research_routes-glm-5.3-baseline-rep7/result.json) |
| [20261028-230611-s11_research_routes-glm-5.3-baseline-rep8](20261028-230611-s11_research_routes-glm-5.3-baseline-rep8/) | s11_research_routes | glm-5.3-baseline | green | 5.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230611-s11_research_routes-glm-5.3-baseline-rep8/metrics.json) · [result](20261028-230611-s11_research_routes-glm-5.3-baseline-rep8/result.json) |
| [20261028-230613-s11_research_routes-glm-5.3-baseline-rep9](20261028-230613-s11_research_routes-glm-5.3-baseline-rep9/) | s11_research_routes | glm-5.3-baseline | green | 5.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230613-s11_research_routes-glm-5.3-baseline-rep9/metrics.json) · [result](20261028-230613-s11_research_routes-glm-5.3-baseline-rep9/result.json) |
| [20261028-230753-s11_research_routes-incredible-four-rep0](20261028-230753-s11_research_routes-incredible-four-rep0/) | s11_research_routes | incredible-four | green | 18.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230753-s11_research_routes-incredible-four-rep0/metrics.json) · [result](20261028-230753-s11_research_routes-incredible-four-rep0/result.json) |
| [20261028-230801-s11_research_routes-incredible-four-rep1](20261028-230801-s11_research_routes-incredible-four-rep1/) | s11_research_routes | incredible-four | green | 21.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230801-s11_research_routes-incredible-four-rep1/metrics.json) · [result](20261028-230801-s11_research_routes-incredible-four-rep1/result.json) |
| [20261028-230804-s11_research_routes-incredible-four-rep2](20261028-230804-s11_research_routes-incredible-four-rep2/) | s11_research_routes | incredible-four | green | 25.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230804-s11_research_routes-incredible-four-rep2/metrics.json) · [result](20261028-230804-s11_research_routes-incredible-four-rep2/result.json) |
| [20261028-230815-s11_research_routes-incredible-four-rep3](20261028-230815-s11_research_routes-incredible-four-rep3/) | s11_research_routes | incredible-four | green | 17.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230815-s11_research_routes-incredible-four-rep3/metrics.json) · [result](20261028-230815-s11_research_routes-incredible-four-rep3/result.json) |
| [20261028-230828-s11_research_routes-incredible-four-rep4](20261028-230828-s11_research_routes-incredible-four-rep4/) | s11_research_routes | incredible-four | green | 32.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230828-s11_research_routes-incredible-four-rep4/metrics.json) · [result](20261028-230828-s11_research_routes-incredible-four-rep4/result.json) |
| [20261028-230834-s11_research_routes-incredible-four-rep5](20261028-230834-s11_research_routes-incredible-four-rep5/) | s11_research_routes | incredible-four | green | 25.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230834-s11_research_routes-incredible-four-rep5/metrics.json) · [result](20261028-230834-s11_research_routes-incredible-four-rep5/result.json) |
| [20261028-230837-s11_research_routes-incredible-four-rep6](20261028-230837-s11_research_routes-incredible-four-rep6/) | s11_research_routes | incredible-four | green | 26.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230837-s11_research_routes-incredible-four-rep6/metrics.json) · [result](20261028-230837-s11_research_routes-incredible-four-rep6/result.json) |
| [20261028-230906-s11_research_routes-incredible-four-rep7](20261028-230906-s11_research_routes-incredible-four-rep7/) | s11_research_routes | incredible-four | green | 24.2 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230906-s11_research_routes-incredible-four-rep7/metrics.json) · [result](20261028-230906-s11_research_routes-incredible-four-rep7/result.json) |
| [20261028-230908-s11_research_routes-incredible-four-rep8](20261028-230908-s11_research_routes-incredible-four-rep8/) | s11_research_routes | incredible-four | green | 26.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230908-s11_research_routes-incredible-four-rep8/metrics.json) · [result](20261028-230908-s11_research_routes-incredible-four-rep8/result.json) |
| [20261028-230909-s11_research_routes-incredible-four-rep9](20261028-230909-s11_research_routes-incredible-four-rep9/) | s11_research_routes | incredible-four | green | 25.1 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230909-s11_research_routes-incredible-four-rep9/metrics.json) · [result](20261028-230909-s11_research_routes-incredible-four-rep9/result.json) |
| [20261028-230936-s11_research_routes-regular-three-rep0](20261028-230936-s11_research_routes-regular-three-rep0/) | s11_research_routes | regular-three | green | 6.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230936-s11_research_routes-regular-three-rep0/metrics.json) · [result](20261028-230936-s11_research_routes-regular-three-rep0/result.json) |
| [20261028-230939-s11_research_routes-regular-three-rep1](20261028-230939-s11_research_routes-regular-three-rep1/) | s11_research_routes | regular-three | green | 6.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230939-s11_research_routes-regular-three-rep1/metrics.json) · [result](20261028-230939-s11_research_routes-regular-three-rep1/result.json) |
| [20261028-230940-s11_research_routes-regular-three-rep2](20261028-230940-s11_research_routes-regular-three-rep2/) | s11_research_routes | regular-three | green | 7.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230940-s11_research_routes-regular-three-rep2/metrics.json) · [result](20261028-230940-s11_research_routes-regular-three-rep2/result.json) |
| [20261028-230953-s11_research_routes-regular-three-rep3](20261028-230953-s11_research_routes-regular-three-rep3/) | s11_research_routes | regular-three | green | 6.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230953-s11_research_routes-regular-three-rep3/metrics.json) · [result](20261028-230953-s11_research_routes-regular-three-rep3/result.json) |
| [20261028-230953-s11_research_routes-regular-three-rep4](20261028-230953-s11_research_routes-regular-three-rep4/) | s11_research_routes | regular-three | green | 6.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230953-s11_research_routes-regular-three-rep4/metrics.json) · [result](20261028-230953-s11_research_routes-regular-three-rep4/result.json) |
| [20261028-230954-s11_research_routes-regular-three-rep5](20261028-230954-s11_research_routes-regular-three-rep5/) | s11_research_routes | regular-three | green | 13.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-230954-s11_research_routes-regular-three-rep5/metrics.json) · [result](20261028-230954-s11_research_routes-regular-three-rep5/result.json) |
| [20261028-231005-s11_research_routes-regular-three-rep6](20261028-231005-s11_research_routes-regular-three-rep6/) | s11_research_routes | regular-three | green | 5.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-231005-s11_research_routes-regular-three-rep6/metrics.json) · [result](20261028-231005-s11_research_routes-regular-three-rep6/result.json) |
| [20261028-231005-s11_research_routes-regular-three-rep7](20261028-231005-s11_research_routes-regular-three-rep7/) | s11_research_routes | regular-three | green | 5.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-231005-s11_research_routes-regular-three-rep7/metrics.json) · [result](20261028-231005-s11_research_routes-regular-three-rep7/result.json) |
| [20261028-231012-s11_research_routes-regular-three-rep8](20261028-231012-s11_research_routes-regular-three-rep8/) | s11_research_routes | regular-three | green | 5.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-231012-s11_research_routes-regular-three-rep8/metrics.json) · [result](20261028-231012-s11_research_routes-regular-three-rep8/result.json) |
| [20261028-231015-s11_research_routes-regular-three-rep9](20261028-231015-s11_research_routes-regular-three-rep9/) | s11_research_routes | regular-three | green | 7.0 s | — | 0/0/0 | 0 | 0 | research:completed | no-testing | clean | [metrics](20261028-231015-s11_research_routes-regular-three-rep9/metrics.json) · [result](20261028-231015-s11_research_routes-regular-three-rep9/result.json) |
| [20261028-231154-s12_research_bug_report-deepseek-v4-baseline-rep0](20261028-231154-s12_research_bug_report-deepseek-v4-baseline-rep0/) | s12_research_bug_report | deepseek-v4-baseline | green | 96.3 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231154-s12_research_bug_report-deepseek-v4-baseline-rep0/metrics.json) · [result](20261028-231154-s12_research_bug_report-deepseek-v4-baseline-rep0/result.json) |
| [20261028-231213-s12_research_bug_report-deepseek-v4-baseline-rep1](20261028-231213-s12_research_bug_report-deepseek-v4-baseline-rep1/) | s12_research_bug_report | deepseek-v4-baseline | green | 90.3 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231213-s12_research_bug_report-deepseek-v4-baseline-rep1/metrics.json) · [result](20261028-231213-s12_research_bug_report-deepseek-v4-baseline-rep1/result.json) |
| [20261028-231216-s12_research_bug_report-deepseek-v4-baseline-rep2](20261028-231216-s12_research_bug_report-deepseek-v4-baseline-rep2/) | s12_research_bug_report | deepseek-v4-baseline | green | 76.3 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-231216-s12_research_bug_report-deepseek-v4-baseline-rep2/metrics.json) · [result](20261028-231216-s12_research_bug_report-deepseek-v4-baseline-rep2/result.json) |
| [20261028-231336-s12_research_bug_report-deepseek-v4-baseline-rep3](20261028-231336-s12_research_bug_report-deepseek-v4-baseline-rep3/) | s12_research_bug_report | deepseek-v4-baseline | green | 84.3 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231336-s12_research_bug_report-deepseek-v4-baseline-rep3/metrics.json) · [result](20261028-231336-s12_research_bug_report-deepseek-v4-baseline-rep3/result.json) |
| [20261028-231339-s12_research_bug_report-deepseek-v4-baseline-rep4](20261028-231339-s12_research_bug_report-deepseek-v4-baseline-rep4/) | s12_research_bug_report | deepseek-v4-baseline | green | 64.3 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231339-s12_research_bug_report-deepseek-v4-baseline-rep4/metrics.json) · [result](20261028-231339-s12_research_bug_report-deepseek-v4-baseline-rep4/result.json) |
| [20261028-231350-s12_research_bug_report-deepseek-v4-baseline-rep5](20261028-231350-s12_research_bug_report-deepseek-v4-baseline-rep5/) | s12_research_bug_report | deepseek-v4-baseline | green | 75.2 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-231350-s12_research_bug_report-deepseek-v4-baseline-rep5/metrics.json) · [result](20261028-231350-s12_research_bug_report-deepseek-v4-baseline-rep5/result.json) |
| [20261028-231452-s12_research_bug_report-deepseek-v4-baseline-rep6](20261028-231452-s12_research_bug_report-deepseek-v4-baseline-rep6/) | s12_research_bug_report | deepseek-v4-baseline | green | 86.3 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231452-s12_research_bug_report-deepseek-v4-baseline-rep6/metrics.json) · [result](20261028-231452-s12_research_bug_report-deepseek-v4-baseline-rep6/result.json) |
| [20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep7](20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep7/) | s12_research_bug_report | deepseek-v4-baseline | green | 74.3 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep7/metrics.json) · [result](20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep7/result.json) |
| [20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep8](20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep8/) | s12_research_bug_report | deepseek-v4-baseline | green | 72.3 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep8/metrics.json) · [result](20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep8/result.json) |
| [20261028-231631-s12_research_bug_report-deepseek-v4-baseline-rep9](20261028-231631-s12_research_bug_report-deepseek-v4-baseline-rep9/) | s12_research_bug_report | deepseek-v4-baseline | green | 88.3 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231631-s12_research_bug_report-deepseek-v4-baseline-rep9/metrics.json) · [result](20261028-231631-s12_research_bug_report-deepseek-v4-baseline-rep9/result.json) |
| [20261028-231015-s12_research_bug_report-glm-5.3-baseline-rep0](20261028-231015-s12_research_bug_report-glm-5.3-baseline-rep0/) | s12_research_bug_report | glm-5.3-baseline | green | 18.1 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-231015-s12_research_bug_report-glm-5.3-baseline-rep0/metrics.json) · [result](20261028-231015-s12_research_bug_report-glm-5.3-baseline-rep0/result.json) |
| [20261028-231023-s12_research_bug_report-glm-5.3-baseline-rep1](20261028-231023-s12_research_bug_report-glm-5.3-baseline-rep1/) | s12_research_bug_report | glm-5.3-baseline | green | 25.1 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231023-s12_research_bug_report-glm-5.3-baseline-rep1/metrics.json) · [result](20261028-231023-s12_research_bug_report-glm-5.3-baseline-rep1/result.json) |
| [20261028-231027-s12_research_bug_report-glm-5.3-baseline-rep2](20261028-231027-s12_research_bug_report-glm-5.3-baseline-rep2/) | s12_research_bug_report | glm-5.3-baseline | green | 19.0 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-231027-s12_research_bug_report-glm-5.3-baseline-rep2/metrics.json) · [result](20261028-231027-s12_research_bug_report-glm-5.3-baseline-rep2/result.json) |
| [20261028-231041-s12_research_bug_report-glm-5.3-baseline-rep3](20261028-231041-s12_research_bug_report-glm-5.3-baseline-rep3/) | s12_research_bug_report | glm-5.3-baseline | green | 40.2 s | — | 0/0/0 | 2 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231041-s12_research_bug_report-glm-5.3-baseline-rep3/metrics.json) · [result](20261028-231041-s12_research_bug_report-glm-5.3-baseline-rep3/result.json) |
| [20261028-231052-s12_research_bug_report-glm-5.3-baseline-rep4](20261028-231052-s12_research_bug_report-glm-5.3-baseline-rep4/) | s12_research_bug_report | glm-5.3-baseline | green | 23.1 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231052-s12_research_bug_report-glm-5.3-baseline-rep4/metrics.json) · [result](20261028-231052-s12_research_bug_report-glm-5.3-baseline-rep4/result.json) |
| [20261028-231054-s12_research_bug_report-glm-5.3-baseline-rep5](20261028-231054-s12_research_bug_report-glm-5.3-baseline-rep5/) | s12_research_bug_report | glm-5.3-baseline | green | 27.1 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-231054-s12_research_bug_report-glm-5.3-baseline-rep5/metrics.json) · [result](20261028-231054-s12_research_bug_report-glm-5.3-baseline-rep5/result.json) |
| [20261028-231122-s12_research_bug_report-glm-5.3-baseline-rep6](20261028-231122-s12_research_bug_report-glm-5.3-baseline-rep6/) | s12_research_bug_report | glm-5.3-baseline | green | 16.1 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231122-s12_research_bug_report-glm-5.3-baseline-rep6/metrics.json) · [result](20261028-231122-s12_research_bug_report-glm-5.3-baseline-rep6/result.json) |
| [20261028-231127-s12_research_bug_report-glm-5.3-baseline-rep7](20261028-231127-s12_research_bug_report-glm-5.3-baseline-rep7/) | s12_research_bug_report | glm-5.3-baseline | green | 21.1 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-231127-s12_research_bug_report-glm-5.3-baseline-rep7/metrics.json) · [result](20261028-231127-s12_research_bug_report-glm-5.3-baseline-rep7/result.json) |
| [20261028-231132-s12_research_bug_report-glm-5.3-baseline-rep8](20261028-231132-s12_research_bug_report-glm-5.3-baseline-rep8/) | s12_research_bug_report | glm-5.3-baseline | failed | 35.3 s | — | 0/0/0 | 2 | 0 | research:completed/bug:Verified successfully/bug:Verified successfully | ok | clean | [metrics](20261028-231132-s12_research_bug_report-glm-5.3-baseline-rep8/metrics.json) · [result](20261028-231132-s12_research_bug_report-glm-5.3-baseline-rep8/result.json) |
| [20261028-231144-s12_research_bug_report-glm-5.3-baseline-rep9](20261028-231144-s12_research_bug_report-glm-5.3-baseline-rep9/) | s12_research_bug_report | glm-5.3-baseline | green | 21.0 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231144-s12_research_bug_report-glm-5.3-baseline-rep9/metrics.json) · [result](20261028-231144-s12_research_bug_report-glm-5.3-baseline-rep9/result.json) |
| [20261028-231631-s12_research_bug_report-incredible-four-rep0](20261028-231631-s12_research_bug_report-incredible-four-rep0/) | s12_research_bug_report | incredible-four | green | 53.2 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231631-s12_research_bug_report-incredible-four-rep0/metrics.json) · [result](20261028-231631-s12_research_bug_report-incredible-four-rep0/result.json) |
| [20261028-231633-s12_research_bug_report-incredible-four-rep1](20261028-231633-s12_research_bug_report-incredible-four-rep1/) | s12_research_bug_report | incredible-four | green | 66.3 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-231633-s12_research_bug_report-incredible-four-rep1/metrics.json) · [result](20261028-231633-s12_research_bug_report-incredible-four-rep1/result.json) |
| [20261028-231737-s12_research_bug_report-incredible-four-rep2](20261028-231737-s12_research_bug_report-incredible-four-rep2/) | s12_research_bug_report | incredible-four | green | 62.4 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231737-s12_research_bug_report-incredible-four-rep2/metrics.json) · [result](20261028-231737-s12_research_bug_report-incredible-four-rep2/result.json) |
| [20261028-231749-s12_research_bug_report-incredible-four-rep3](20261028-231749-s12_research_bug_report-incredible-four-rep3/) | s12_research_bug_report | incredible-four | green | 71.4 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-231749-s12_research_bug_report-incredible-four-rep3/metrics.json) · [result](20261028-231749-s12_research_bug_report-incredible-four-rep3/result.json) |
| [20261028-231812-s12_research_bug_report-incredible-four-rep4](20261028-231812-s12_research_bug_report-incredible-four-rep4/) | s12_research_bug_report | incredible-four | green | 55.4 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-231812-s12_research_bug_report-incredible-four-rep4/metrics.json) · [result](20261028-231812-s12_research_bug_report-incredible-four-rep4/result.json) |
| [20261028-231850-s12_research_bug_report-incredible-four-rep5](20261028-231850-s12_research_bug_report-incredible-four-rep5/) | s12_research_bug_report | incredible-four | green | 80.3 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231850-s12_research_bug_report-incredible-four-rep5/metrics.json) · [result](20261028-231850-s12_research_bug_report-incredible-four-rep5/result.json) |
| [20261028-231908-s12_research_bug_report-incredible-four-rep6](20261028-231908-s12_research_bug_report-incredible-four-rep6/) | s12_research_bug_report | incredible-four | green | 58.2 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231908-s12_research_bug_report-incredible-four-rep6/metrics.json) · [result](20261028-231908-s12_research_bug_report-incredible-four-rep6/result.json) |
| [20261028-231913-s12_research_bug_report-incredible-four-rep7](20261028-231913-s12_research_bug_report-incredible-four-rep7/) | s12_research_bug_report | incredible-four | green | 61.1 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-231913-s12_research_bug_report-incredible-four-rep7/metrics.json) · [result](20261028-231913-s12_research_bug_report-incredible-four-rep7/result.json) |
| [20261028-232012-s12_research_bug_report-incredible-four-rep8](20261028-232012-s12_research_bug_report-incredible-four-rep8/) | s12_research_bug_report | incredible-four | green | 63.1 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-232012-s12_research_bug_report-incredible-four-rep8/metrics.json) · [result](20261028-232012-s12_research_bug_report-incredible-four-rep8/result.json) |
| [20261028-232021-s12_research_bug_report-incredible-four-rep9](20261028-232021-s12_research_bug_report-incredible-four-rep9/) | s12_research_bug_report | incredible-four | green | 54.2 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-232021-s12_research_bug_report-incredible-four-rep9/metrics.json) · [result](20261028-232021-s12_research_bug_report-incredible-four-rep9/result.json) |
| [20261028-232021-s12_research_bug_report-regular-three-rep0](20261028-232021-s12_research_bug_report-regular-three-rep0/) | s12_research_bug_report | regular-three | green | 23.1 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-232021-s12_research_bug_report-regular-three-rep0/metrics.json) · [result](20261028-232021-s12_research_bug_report-regular-three-rep0/result.json) |
| [20261028-232050-s12_research_bug_report-regular-three-rep1](20261028-232050-s12_research_bug_report-regular-three-rep1/) | s12_research_bug_report | regular-three | green | 26.2 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-232050-s12_research_bug_report-regular-three-rep1/metrics.json) · [result](20261028-232050-s12_research_bug_report-regular-three-rep1/result.json) |
| [20261028-232122-s12_research_bug_report-regular-three-rep2](20261028-232122-s12_research_bug_report-regular-three-rep2/) | s12_research_bug_report | regular-three | green | 26.1 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-232122-s12_research_bug_report-regular-three-rep2/metrics.json) · [result](20261028-232122-s12_research_bug_report-regular-three-rep2/result.json) |
| [20261028-232123-s12_research_bug_report-regular-three-rep3](20261028-232123-s12_research_bug_report-regular-three-rep3/) | s12_research_bug_report | regular-three | green | 20.1 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-232123-s12_research_bug_report-regular-three-rep3/metrics.json) · [result](20261028-232123-s12_research_bug_report-regular-three-rep3/result.json) |
| [20261028-232127-s12_research_bug_report-regular-three-rep4](20261028-232127-s12_research_bug_report-regular-three-rep4/) | s12_research_bug_report | regular-three | green | 18.0 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-232127-s12_research_bug_report-regular-three-rep4/metrics.json) · [result](20261028-232127-s12_research_bug_report-regular-three-rep4/result.json) |
| [20261028-232154-s12_research_bug_report-regular-three-rep5](20261028-232154-s12_research_bug_report-regular-three-rep5/) | s12_research_bug_report | regular-three | green | 17.2 s | — | 0/0/0 | 1 | 0 | bug:Verified successfully/research:completed | ok | clean | [metrics](20261028-232154-s12_research_bug_report-regular-three-rep5/metrics.json) · [result](20261028-232154-s12_research_bug_report-regular-three-rep5/result.json) |
| [20261028-232155-s12_research_bug_report-regular-three-rep6](20261028-232155-s12_research_bug_report-regular-three-rep6/) | s12_research_bug_report | regular-three | failed | 34.3 s | — | 0/0/0 | 2 | 0 | bug:Verified successfully/research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-232155-s12_research_bug_report-regular-three-rep6/metrics.json) · [result](20261028-232155-s12_research_bug_report-regular-three-rep6/result.json) |
| [20261028-232201-s12_research_bug_report-regular-three-rep7](20261028-232201-s12_research_bug_report-regular-three-rep7/) | s12_research_bug_report | regular-three | green | 21.1 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-232201-s12_research_bug_report-regular-three-rep7/metrics.json) · [result](20261028-232201-s12_research_bug_report-regular-three-rep7/result.json) |
| [20261028-232218-s12_research_bug_report-regular-three-rep8](20261028-232218-s12_research_bug_report-regular-three-rep8/) | s12_research_bug_report | regular-three | green | 18.0 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-232218-s12_research_bug_report-regular-three-rep8/metrics.json) · [result](20261028-232218-s12_research_bug_report-regular-three-rep8/result.json) |
| [20261028-232229-s12_research_bug_report-regular-three-rep9](20261028-232229-s12_research_bug_report-regular-three-rep9/) | s12_research_bug_report | regular-three | green | 17.0 s | — | 0/0/0 | 1 | 0 | research:completed/bug:Verified successfully | ok | clean | [metrics](20261028-232229-s12_research_bug_report-regular-three-rep9/metrics.json) · [result](20261028-232229-s12_research_bug_report-regular-three-rep9/result.json) |
| [20261028-232423-s13_research_feature-deepseek-v4-baseline-rep0](20261028-232423-s13_research_feature-deepseek-v4-baseline-rep0/) | s13_research_feature | deepseek-v4-baseline | green | 122.3 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-232423-s13_research_feature-deepseek-v4-baseline-rep0/metrics.json) · [result](20261028-232423-s13_research_feature-deepseek-v4-baseline-rep0/result.json) |
| [20261028-232428-s13_research_feature-deepseek-v4-baseline-rep1](20261028-232428-s13_research_feature-deepseek-v4-baseline-rep1/) | s13_research_feature | deepseek-v4-baseline | green | 125.4 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-232428-s13_research_feature-deepseek-v4-baseline-rep1/metrics.json) · [result](20261028-232428-s13_research_feature-deepseek-v4-baseline-rep1/result.json) |
| [20261028-232454-s13_research_feature-deepseek-v4-baseline-rep2](20261028-232454-s13_research_feature-deepseek-v4-baseline-rep2/) | s13_research_feature | deepseek-v4-baseline | green | 116.3 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-232454-s13_research_feature-deepseek-v4-baseline-rep2/metrics.json) · [result](20261028-232454-s13_research_feature-deepseek-v4-baseline-rep2/result.json) |
| [20261028-232631-s13_research_feature-deepseek-v4-baseline-rep3](20261028-232631-s13_research_feature-deepseek-v4-baseline-rep3/) | s13_research_feature | deepseek-v4-baseline | green | 145.4 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-232631-s13_research_feature-deepseek-v4-baseline-rep3/metrics.json) · [result](20261028-232631-s13_research_feature-deepseek-v4-baseline-rep3/result.json) |
| [20261028-232639-s13_research_feature-deepseek-v4-baseline-rep4](20261028-232639-s13_research_feature-deepseek-v4-baseline-rep4/) | s13_research_feature | deepseek-v4-baseline | green | 134.5 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-232639-s13_research_feature-deepseek-v4-baseline-rep4/metrics.json) · [result](20261028-232639-s13_research_feature-deepseek-v4-baseline-rep4/result.json) |
| [20261028-232700-s13_research_feature-deepseek-v4-baseline-rep5](20261028-232700-s13_research_feature-deepseek-v4-baseline-rep5/) | s13_research_feature | deepseek-v4-baseline | green | 124.4 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-232700-s13_research_feature-deepseek-v4-baseline-rep5/metrics.json) · [result](20261028-232700-s13_research_feature-deepseek-v4-baseline-rep5/result.json) |
| [20261028-232900-s13_research_feature-deepseek-v4-baseline-rep6](20261028-232900-s13_research_feature-deepseek-v4-baseline-rep6/) | s13_research_feature | deepseek-v4-baseline | green | 100.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-232900-s13_research_feature-deepseek-v4-baseline-rep6/metrics.json) · [result](20261028-232900-s13_research_feature-deepseek-v4-baseline-rep6/result.json) |
| [20261028-232907-s13_research_feature-deepseek-v4-baseline-rep7](20261028-232907-s13_research_feature-deepseek-v4-baseline-rep7/) | s13_research_feature | deepseek-v4-baseline | green | 111.3 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-232907-s13_research_feature-deepseek-v4-baseline-rep7/metrics.json) · [result](20261028-232907-s13_research_feature-deepseek-v4-baseline-rep7/result.json) |
| [20261028-232910-s13_research_feature-deepseek-v4-baseline-rep8](20261028-232910-s13_research_feature-deepseek-v4-baseline-rep8/) | s13_research_feature | deepseek-v4-baseline | green | 109.4 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-232910-s13_research_feature-deepseek-v4-baseline-rep8/metrics.json) · [result](20261028-232910-s13_research_feature-deepseek-v4-baseline-rep8/result.json) |
| [20261028-233049-s13_research_feature-deepseek-v4-baseline-rep9](20261028-233049-s13_research_feature-deepseek-v4-baseline-rep9/) | s13_research_feature | deepseek-v4-baseline | green | 115.4 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233049-s13_research_feature-deepseek-v4-baseline-rep9/metrics.json) · [result](20261028-233049-s13_research_feature-deepseek-v4-baseline-rep9/result.json) |
| [20261028-232236-s13_research_feature-glm-5.3-baseline-rep0](20261028-232236-s13_research_feature-glm-5.3-baseline-rep0/) | s13_research_feature | glm-5.3-baseline | green | 24.1 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-232236-s13_research_feature-glm-5.3-baseline-rep0/metrics.json) · [result](20261028-232236-s13_research_feature-glm-5.3-baseline-rep0/result.json) |
| [20261028-232242-s13_research_feature-glm-5.3-baseline-rep1](20261028-232242-s13_research_feature-glm-5.3-baseline-rep1/) | s13_research_feature | glm-5.3-baseline | green | 21.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-232242-s13_research_feature-glm-5.3-baseline-rep1/metrics.json) · [result](20261028-232242-s13_research_feature-glm-5.3-baseline-rep1/result.json) |
| [20261028-232257-s13_research_feature-glm-5.3-baseline-rep2](20261028-232257-s13_research_feature-glm-5.3-baseline-rep2/) | s13_research_feature | glm-5.3-baseline | green | 21.0 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-232257-s13_research_feature-glm-5.3-baseline-rep2/metrics.json) · [result](20261028-232257-s13_research_feature-glm-5.3-baseline-rep2/result.json) |
| [20261028-232307-s13_research_feature-glm-5.3-baseline-rep3](20261028-232307-s13_research_feature-glm-5.3-baseline-rep3/) | s13_research_feature | glm-5.3-baseline | green | 24.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-232307-s13_research_feature-glm-5.3-baseline-rep3/metrics.json) · [result](20261028-232307-s13_research_feature-glm-5.3-baseline-rep3/result.json) |
| [20261028-232310-s13_research_feature-glm-5.3-baseline-rep4](20261028-232310-s13_research_feature-glm-5.3-baseline-rep4/) | s13_research_feature | glm-5.3-baseline | green | 19.1 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-232310-s13_research_feature-glm-5.3-baseline-rep4/metrics.json) · [result](20261028-232310-s13_research_feature-glm-5.3-baseline-rep4/result.json) |
| [20261028-232324-s13_research_feature-glm-5.3-baseline-rep5](20261028-232324-s13_research_feature-glm-5.3-baseline-rep5/) | s13_research_feature | glm-5.3-baseline | green | 22.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-232324-s13_research_feature-glm-5.3-baseline-rep5/metrics.json) · [result](20261028-232324-s13_research_feature-glm-5.3-baseline-rep5/result.json) |
| [20261028-232336-s13_research_feature-glm-5.3-baseline-rep6](20261028-232336-s13_research_feature-glm-5.3-baseline-rep6/) | s13_research_feature | glm-5.3-baseline | green | 35.1 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-232336-s13_research_feature-glm-5.3-baseline-rep6/metrics.json) · [result](20261028-232336-s13_research_feature-glm-5.3-baseline-rep6/result.json) |
| [20261028-232340-s13_research_feature-glm-5.3-baseline-rep7](20261028-232340-s13_research_feature-glm-5.3-baseline-rep7/) | s13_research_feature | glm-5.3-baseline | green | 31.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-232340-s13_research_feature-glm-5.3-baseline-rep7/metrics.json) · [result](20261028-232340-s13_research_feature-glm-5.3-baseline-rep7/result.json) |
| [20261028-232353-s13_research_feature-glm-5.3-baseline-rep8](20261028-232353-s13_research_feature-glm-5.3-baseline-rep8/) | s13_research_feature | glm-5.3-baseline | green | 28.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-232353-s13_research_feature-glm-5.3-baseline-rep8/metrics.json) · [result](20261028-232353-s13_research_feature-glm-5.3-baseline-rep8/result.json) |
| [20261028-232419-s13_research_feature-glm-5.3-baseline-rep9](20261028-232419-s13_research_feature-glm-5.3-baseline-rep9/) | s13_research_feature | glm-5.3-baseline | green | 28.1 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-232419-s13_research_feature-glm-5.3-baseline-rep9/metrics.json) · [result](20261028-232419-s13_research_feature-glm-5.3-baseline-rep9/result.json) |
| [20261028-233104-s13_research_feature-incredible-four-rep0](20261028-233104-s13_research_feature-incredible-four-rep0/) | s13_research_feature | incredible-four | green | 61.3 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233104-s13_research_feature-incredible-four-rep0/metrics.json) · [result](20261028-233104-s13_research_feature-incredible-four-rep0/result.json) |
| [20261028-233105-s13_research_feature-incredible-four-rep1](20261028-233105-s13_research_feature-incredible-four-rep1/) | s13_research_feature | incredible-four | green | 50.1 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233105-s13_research_feature-incredible-four-rep1/metrics.json) · [result](20261028-233105-s13_research_feature-incredible-four-rep1/result.json) |
| [20261028-233201-s13_research_feature-incredible-four-rep2](20261028-233201-s13_research_feature-incredible-four-rep2/) | s13_research_feature | incredible-four | green | 67.3 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233201-s13_research_feature-incredible-four-rep2/metrics.json) · [result](20261028-233201-s13_research_feature-incredible-four-rep2/result.json) |
| [20261028-233211-s13_research_feature-incredible-four-rep3](20261028-233211-s13_research_feature-incredible-four-rep3/) | s13_research_feature | incredible-four | green | 52.1 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233211-s13_research_feature-incredible-four-rep3/metrics.json) · [result](20261028-233211-s13_research_feature-incredible-four-rep3/result.json) |
| [20261028-233258-s13_research_feature-incredible-four-rep4](20261028-233258-s13_research_feature-incredible-four-rep4/) | s13_research_feature | incredible-four | green | 67.2 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233258-s13_research_feature-incredible-four-rep4/metrics.json) · [result](20261028-233258-s13_research_feature-incredible-four-rep4/result.json) |
| [20261028-233309-s13_research_feature-incredible-four-rep5](20261028-233309-s13_research_feature-incredible-four-rep5/) | s13_research_feature | incredible-four | green | 59.4 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233309-s13_research_feature-incredible-four-rep5/metrics.json) · [result](20261028-233309-s13_research_feature-incredible-four-rep5/result.json) |
| [20261028-233320-s13_research_feature-incredible-four-rep6](20261028-233320-s13_research_feature-incredible-four-rep6/) | s13_research_feature | incredible-four | green | 61.2 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233320-s13_research_feature-incredible-four-rep6/metrics.json) · [result](20261028-233320-s13_research_feature-incredible-four-rep6/result.json) |
| [20261028-233412-s13_research_feature-incredible-four-rep7](20261028-233412-s13_research_feature-incredible-four-rep7/) | s13_research_feature | incredible-four | green | 58.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-233412-s13_research_feature-incredible-four-rep7/metrics.json) · [result](20261028-233412-s13_research_feature-incredible-four-rep7/result.json) |
| [20261028-233418-s13_research_feature-incredible-four-rep8](20261028-233418-s13_research_feature-incredible-four-rep8/) | s13_research_feature | incredible-four | green | 57.2 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233418-s13_research_feature-incredible-four-rep8/metrics.json) · [result](20261028-233418-s13_research_feature-incredible-four-rep8/result.json) |
| [20261028-233427-s13_research_feature-incredible-four-rep9](20261028-233427-s13_research_feature-incredible-four-rep9/) | s13_research_feature | incredible-four | green | 67.3 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233427-s13_research_feature-incredible-four-rep9/metrics.json) · [result](20261028-233427-s13_research_feature-incredible-four-rep9/result.json) |
| [20261028-233520-s13_research_feature-regular-three-rep0](20261028-233520-s13_research_feature-regular-three-rep0/) | s13_research_feature | regular-three | green | 22.2 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-233520-s13_research_feature-regular-three-rep0/metrics.json) · [result](20261028-233520-s13_research_feature-regular-three-rep0/result.json) |
| [20261028-233521-s13_research_feature-regular-three-rep1](20261028-233521-s13_research_feature-regular-three-rep1/) | s13_research_feature | regular-three | green | 28.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-233521-s13_research_feature-regular-three-rep1/metrics.json) · [result](20261028-233521-s13_research_feature-regular-three-rep1/result.json) |
| [20261028-233540-s13_research_feature-regular-three-rep2](20261028-233540-s13_research_feature-regular-three-rep2/) | s13_research_feature | regular-three | green | 23.1 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233540-s13_research_feature-regular-three-rep2/metrics.json) · [result](20261028-233540-s13_research_feature-regular-three-rep2/result.json) |
| [20261028-233552-s13_research_feature-regular-three-rep3](20261028-233552-s13_research_feature-regular-three-rep3/) | s13_research_feature | regular-three | green | 22.3 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233552-s13_research_feature-regular-three-rep3/metrics.json) · [result](20261028-233552-s13_research_feature-regular-three-rep3/result.json) |
| [20261028-233558-s13_research_feature-regular-three-rep4](20261028-233558-s13_research_feature-regular-three-rep4/) | s13_research_feature | regular-three | green | 23.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-233558-s13_research_feature-regular-three-rep4/metrics.json) · [result](20261028-233558-s13_research_feature-regular-three-rep4/result.json) |
| [20261028-233609-s13_research_feature-regular-three-rep5](20261028-233609-s13_research_feature-regular-three-rep5/) | s13_research_feature | regular-three | green | 21.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-233609-s13_research_feature-regular-three-rep5/metrics.json) · [result](20261028-233609-s13_research_feature-regular-three-rep5/result.json) |
| [20261028-233620-s13_research_feature-regular-three-rep6](20261028-233620-s13_research_feature-regular-three-rep6/) | s13_research_feature | regular-three | green | 20.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-233620-s13_research_feature-regular-three-rep6/metrics.json) · [result](20261028-233620-s13_research_feature-regular-three-rep6/result.json) |
| [20261028-233628-s13_research_feature-regular-three-rep7](20261028-233628-s13_research_feature-regular-three-rep7/) | s13_research_feature | regular-three | green | 23.1 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-233628-s13_research_feature-regular-three-rep7/metrics.json) · [result](20261028-233628-s13_research_feature-regular-three-rep7/result.json) |
| [20261028-233637-s13_research_feature-regular-three-rep8](20261028-233637-s13_research_feature-regular-three-rep8/) | s13_research_feature | regular-three | green | 21.1 s | — | 0/0/0 | 1 | 0 | research:completed/feature:Verified successfully | ok | clean | [metrics](20261028-233637-s13_research_feature-regular-three-rep8/metrics.json) · [result](20261028-233637-s13_research_feature-regular-three-rep8/result.json) |
| [20261028-233646-s13_research_feature-regular-three-rep9](20261028-233646-s13_research_feature-regular-three-rep9/) | s13_research_feature | regular-three | green | 21.0 s | — | 0/0/0 | 1 | 0 | feature:Verified successfully/research:completed | ok | clean | [metrics](20261028-233646-s13_research_feature-regular-three-rep9/metrics.json) · [result](20261028-233646-s13_research_feature-regular-three-rep9/result.json) |

## Run details

### 20261028-233755-s1_happy-deepseek-v4-baseline-rep0 — s1_happy × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 10.6 | 25.7 | 35.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 36.464 | 4.013 | 6.8022 | 29858 | 1188 |

Overall: 9 model requests, latency p50 4.013 s / p95 6.8022 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233755-s1_happy-deepseek-v4-baseline-rep0/`

### 20261028-233812-s1_happy-deepseek-v4-baseline-rep1 — s1_happy × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 12.6 | 22.6 | 34.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 35.355 | 4.284 | 4.7146 | 29635 | 1124 |

Overall: 9 model requests, latency p50 4.284 s / p95 4.7146 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233812-s1_happy-deepseek-v4-baseline-rep1/`

### 20261028-233816-s1_happy-deepseek-v4-baseline-rep2 — s1_happy × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 12.6 | 21.5 | 33.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 32.355 | 3.476 | 5.409 | 30079 | 1031 |

Overall: 9 model requests, latency p50 3.476 s / p95 5.409 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233816-s1_happy-deepseek-v4-baseline-rep2/`

### 20261028-233841-s1_happy-deepseek-v4-baseline-rep3 — s1_happy × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 10 | 26.8 | 35.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 34.161 | 3.129 | 6.3984 | 30735 | 1217 |

Overall: 9 model requests, latency p50 3.129 s / p95 6.3984 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233841-s1_happy-deepseek-v4-baseline-rep3/`

### 20261028-233857-s1_happy-deepseek-v4-baseline-rep4 — s1_happy × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 11.6 | 31.2 | 39.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 38.306 | 3.644 | 7.2708 | 29591 | 1087 |

Overall: 9 model requests, latency p50 3.644 s / p95 7.2708 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233857-s1_happy-deepseek-v4-baseline-rep4/`

### 20261028-233858-s1_happy-deepseek-v4-baseline-rep5 — s1_happy × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 10.9 | 29.8 | 37.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 10 | 39.447 | 3.4525 | 6.7806 | 33028 | 1086 |

Overall: 10 model requests, latency p50 3.4525 s / p95 6.7806 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233858-s1_happy-deepseek-v4-baseline-rep5/`

### 20261028-233931-s1_happy-deepseek-v4-baseline-rep6 — s1_happy × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 18.2 | 18.6 | 36.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 36.399 | 3.887 | 6.0744 | 28031 | 856 |

Overall: 9 model requests, latency p50 3.887 s / p95 6.0744 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233931-s1_happy-deepseek-v4-baseline-rep6/`

### 20261028-233948-s1_happy-deepseek-v4-baseline-rep7 — s1_happy × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 13.6 | 53.5 | 66.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 66.325 | 5.455 | 15.8668 | 30297 | 1569 |

Overall: 9 model requests, latency p50 5.455 s / p95 15.8668 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233948-s1_happy-deepseek-v4-baseline-rep7/`

### 20261028-233949-s1_happy-deepseek-v4-baseline-rep8 — s1_happy × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 14.6 | 59.4 | 73.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 10 | 72.599 | 4.2695 | 20.2274 | 34181 | 1348 |

Overall: 10 model requests, latency p50 4.2695 s / p95 20.2274 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233949-s1_happy-deepseek-v4-baseline-rep8/`

### 20261028-234017-s1_happy-deepseek-v4-baseline-rep9 — s1_happy × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 50.5 | 178.9 | 228.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 232.27 | 6.493 | 99.7304 | 29172 | 988 |

Overall: 9 model requests, latency p50 6.493 s / p95 99.7304 s.
Recorder ↔ transcript cross-check: 8/9 transcript responses matched, 1 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261028-234017-s1_happy-deepseek-v4-baseline-rep9/`

### 20261028-233701-s1_happy-glm-5.3-baseline-rep0 — s1_happy × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4 | 7 | 10.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 7.099 | 0.74 | 1.0932 | 28137 | 617 |

Overall: 9 model requests, latency p50 0.74 s / p95 1.0932 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233701-s1_happy-glm-5.3-baseline-rep0/`

### 20261028-233704-s1_happy-glm-5.3-baseline-rep1 — s1_happy × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4.3 | 6.4 | 10.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 7.572 | 0.734 | 1.0113 | 30121 | 594 |

Overall: 10 model requests, latency p50 0.734 s / p95 1.0113 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233704-s1_happy-glm-5.3-baseline-rep1/`

### 20261028-233713-s1_happy-glm-5.3-baseline-rep2 — s1_happy × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4.3 | 5.2 | 9.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 6.4 | 0.599 | 1.117 | 26699 | 509 |

Overall: 9 model requests, latency p50 0.599 s / p95 1.117 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233713-s1_happy-glm-5.3-baseline-rep2/`

### 20261028-233720-s1_happy-glm-5.3-baseline-rep3 — s1_happy × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 3.9 | 5.4 | 8.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 6.231 | 0.66 | 1.0606 | 27736 | 516 |

Overall: 9 model requests, latency p50 0.66 s / p95 1.0606 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233720-s1_happy-glm-5.3-baseline-rep3/`

### 20261028-233722-s1_happy-glm-5.3-baseline-rep4 — s1_happy × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4 | 7 | 10.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 8.245 | 0.791 | 1.7904 | 47192 | 815 |

Overall: 9 model requests, latency p50 0.791 s / p95 1.7904 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233722-s1_happy-glm-5.3-baseline-rep4/`

### 20261028-233730-s1_happy-glm-5.3-baseline-rep5 — s1_happy × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 3.9 | 11.1 | 14.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 11 | 8.72 | 0.671 | 1.333 | 34357 | 819 |

Overall: 11 model requests, latency p50 0.671 s / p95 1.333 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233730-s1_happy-glm-5.3-baseline-rep5/`

### 20261028-233736-s1_happy-glm-5.3-baseline-rep6 — s1_happy × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 3.7 | 5.6 | 8.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 6.507 | 0.663 | 1.016 | 26730 | 503 |

Overall: 9 model requests, latency p50 0.663 s / p95 1.016 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233736-s1_happy-glm-5.3-baseline-rep6/`

### 20261028-233740-s1_happy-glm-5.3-baseline-rep7 — s1_happy × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 3.7 | 5 | 8.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 5.634 | 0.554 | 0.8808 | 25503 | 434 |

Overall: 9 model requests, latency p50 0.554 s / p95 0.8808 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233740-s1_happy-glm-5.3-baseline-rep7/`

### 20261028-233752-s1_happy-glm-5.3-baseline-rep8 — s1_happy × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4 | 7.7 | 10.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 8.928 | 0.6965 | 1.6388 | 29337 | 526 |

Overall: 10 model requests, latency p50 0.6965 s / p95 1.6388 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233752-s1_happy-glm-5.3-baseline-rep8/`

### 20261028-233755-s1_happy-glm-5.3-baseline-rep9 — s1_happy × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4 | 9.2 | 12.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 10.697 | 0.7645 | 2.5069 | 29873 | 631 |

Overall: 10 model requests, latency p50 0.7645 s / p95 2.5069 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233755-s1_happy-glm-5.3-baseline-rep9/`

### 20261028-234109-s1_happy-incredible-four-rep0 — s1_happy × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 31.9 | 55.4 | 86.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 30.637 | 3.5185 | 19.5623 | 11022 | 150 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 54.033 | 1.775 | 32.385 | 20496 | 1207 |

Overall: 9 model requests, latency p50 1.775 s / p95 31.1948 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-234109-s1_happy-incredible-four-rep0/`

### 20261028-234113-s1_happy-incredible-four-rep1 — s1_happy × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 33.6 | 83.5 | 116.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 31.09 | 4.7115 | 19.0793 | 11050 | 189 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 79.778 | 4.4185 | 33.6377 | 37688 | 2709 |

Overall: 12 model requests, latency p50 4.4185 s / p95 30.6115 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-234113-s1_happy-incredible-four-rep1/`

### 20261028-234249-s1_happy-incredible-four-rep2 — s1_happy × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 8.2 | 33.4 | 40.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 6.872 | 0.546 | 4.611 | 11030 | 167 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 31.844 | 2.165 | 12.6088 | 67428 | 2485 |

Overall: 11 model requests, latency p50 1.633 s / p95 11.69 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-234249-s1_happy-incredible-four-rep2/`

### 20261028-234318-s1_happy-incredible-four-rep3 — s1_happy × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4.1 | 30.8 | 34.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.972 | 0.74 | 0.8591 | 11026 | 164 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 27.861 | 2.372 | 8.8645 | 26910 | 1314 |

Overall: 11 model requests, latency p50 1.148 s / p95 8.5115 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-234318-s1_happy-incredible-four-rep3/`

### 20261028-234340-s1_happy-incredible-four-rep4 — s1_happy × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 12.3 | 898.6 | 910.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 9.795 | 1.5865 | 5.5973 | 11050 | 169 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 695.798 | 2.003 | 407.672 | 40126 | 2134 |

Overall: 13 model requests, latency p50 2.003 s / p95 275.998 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-234340-s1_happy-incredible-four-rep4/`

### 20261028-234400-s1_happy-incredible-four-rep5 — s1_happy × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4 | 254 | 257.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.59 | 0.6315 | 0.7054 | 11022 | 167 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 277.358 | 18.369 | 141.414 | 45951 | 2632 |

Overall: 11 model requests, latency p50 5.68 s / p95 108.971 s.
Recorder ↔ transcript cross-check: 10/11 transcript responses matched, 1 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261028-234400-s1_happy-incredible-four-rep5/`

### 20261028-234420-s1_happy-incredible-four-rep6 — s1_happy × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 11.5 | 52.9 | 63.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 10.331 | 2.2305 | 5.1326 | 11040 | 162 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 48.961 | 1.5245 | 29.3155 | 53241 | 1401 |

Overall: 10 model requests, latency p50 1.5245 s / p95 23.5079 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-234420-s1_happy-incredible-four-rep6/`

### 20261028-234531-s1_happy-incredible-four-rep7 — s1_happy × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 84.3 | 22 | 105.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 82.952 | 2.282 | 66.8243 | 11033 | 153 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 16.909 | 1.741 | 8.2328 | 20013 | 1115 |

Overall: 9 model requests, latency p50 1.741 s / p95 50.5154 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-234531-s1_happy-incredible-four-rep7/`

### 20261028-234730-s1_happy-incredible-four-rep8 — s1_happy × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 8.4 | 678.1 | 685.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 7.136 | 0.8015 | 4.3692 | 11029 | 175 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 671.412 | 5.233 | 403.908 | 68476 | 2054 |

Overall: 12 model requests, latency p50 3.876 s / p95 291.256 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-234730-s1_happy-incredible-four-rep8/`

### 20261028-234856-s1_happy-incredible-four-rep9 — s1_happy × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 12.6 | 627.9 | 639.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 11.428 | 2.418 | 5.8062 | 11063 | 181 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 11 | 619.433 | 1.583 | 302.407 | 48659 | 2659 |

Overall: 15 model requests, latency p50 1.583 s / p95 184.394 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-234856-s1_happy-incredible-four-rep9/`

### 20261028-235902-s1_happy-regular-three-rep0 — s1_happy × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4.9 | 6.3 | 10.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 3.824 | 0.6305 | 1.8669 | 11029 | 175 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 4.086 | 0.7015 | 0.735 | 21595 | 397 |

Overall: 10 model requests, latency p50 0.7015 s / p95 1.4714 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-235902-s1_happy-regular-three-rep0/`

### 20261028-235908-s1_happy-regular-three-rep1 — s1_happy × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 3.9 | 7.6 | 11.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.832 | 0.644 | 1.0651 | 11061 | 179 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 5.61 | 0.6585 | 1.0205 | 33214 | 608 |

Overall: 12 model requests, latency p50 0.6585 s / p95 1.1405 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-235908-s1_happy-regular-three-rep1/`

### 20261028-235926-s1_happy-regular-three-rep2 — s1_happy × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 3.8 | 9.2 | 9.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.481 | 0.6275 | 0.6988 | 11050 | 175 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 9 | 5.929 | 0.614 | 0.9916 | 31230 | 571 |

Overall: 13 model requests, latency p50 0.614 s / p95 0.9244 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-235926-s1_happy-regular-three-rep2/`

### 20261028-235927-s1_happy-regular-three-rep3 — s1_happy × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 3.9 | 5.1 | 8.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.608 | 0.6525 | 0.7849 | 11025 | 159 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 5 | 3.545 | 0.653 | 1.0444 | 17407 | 301 |

Overall: 9 model requests, latency p50 0.653 s / p95 1.0038 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-235927-s1_happy-regular-three-rep3/`

### 20261028-235943-s1_happy-regular-three-rep4 — s1_happy × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 5.1 | 6.1 | 10.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 4.037 | 0.8615 | 1.6369 | 11062 | 177 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.225 | 0.66 | 1.3728 | 15699 | 317 |

Overall: 9 model requests, latency p50 0.789 s / p95 1.6638 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-235943-s1_happy-regular-three-rep4/`

### 20261028-235947-s1_happy-regular-three-rep5 — s1_happy × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4.1 | 10.5 | 14.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 5.244 | 0.754 | 2.895 | 11050 | 189 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 4.24 | 0.702 | 0.9585 | 18942 | 365 |

Overall: 10 model requests, latency p50 0.738 s / p95 2.2439 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-235947-s1_happy-regular-three-rep5/`

### 20261028-235947-s1_happy-regular-three-rep6 — s1_happy × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 3.9 | 5.5 | 9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.736 | 0.69 | 0.823 | 11074 | 188 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 5 | 3.846 | 0.812 | 0.9624 | 16017 | 387 |

Overall: 9 model requests, latency p50 0.795 s / p95 0.9418 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-235947-s1_happy-regular-three-rep6/`

### 20261029-000003-s1_happy-regular-three-rep7 — s1_happy × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 5.2 | 8.6 | 13.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 5.799 | 0.8315 | 3.1351 | 11022 | 164 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 4.09 | 0.6525 | 0.9998 | 19313 | 428 |

Overall: 10 model requests, latency p50 0.78 s / p95 2.4235 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000003-s1_happy-regular-three-rep7/`

### 20261029-000003-s1_happy-regular-three-rep8 — s1_happy × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 5.2 | 8.3 | 13.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 5.761 | 0.806 | 3.1074 | 11029 | 168 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 3.987 | 0.6725 | 0.7528 | 21858 | 346 |

Overall: 10 model requests, latency p50 0.721 s / p95 2.3103 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000003-s1_happy-regular-three-rep8/`

### 20261029-000008-s1_happy-regular-three-rep9 — s1_happy × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным | feature | completed | Verified successfully | 4.5 | 5.3 | 9.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.917 | 0.7295 | 0.9463 | 11071 | 180 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 3.483 | 0.601 | 0.6898 | 18727 | 292 |

Overall: 10 model requests, latency p50 0.6455 s / p95 0.9049 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000008-s1_happy-regular-three-rep9/`

### 20261029-000301-s2a_bug_followup-deepseek-v4-baseline-rep0 — s2a_bug_followup × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 39.6 | 23.2 | 200.9 |
| pct() returns 0.25 instead of 25.0 (missing * 100) | bug | completed | Verified successfully | 34.1 | 26.6 | 73.2 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:04:07.456317+00:00', 'detail': 'coder message at 2026-10-28T21:04:07.456317+00:00 inside tester interval 2026-10-28T21:03:34.593909+00:00…2026-10-28T21:04:08.243654+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() returns 0.25 instead of 25.0 (missing * 100)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:04:07.086232+00:00', 'detail': 'coder message at 2026-10-28T21:04:07.086232+00:00 inside tester interval 2026-10-28T21:03:34.593909+00:00…2026-10-28T21:04:08.243654+00:00'}

Bug round-trips:

- `a7f522c2` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:05:24.443522+00:00)
- `cf08d6c4` pct() returns 0.25 instead of 25.0 (missing * 100) (activated 2026-10-28T21:04:20.176245+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 30 | 192.972 | 4.665 | 17.4994 | 108292 | 6397 |

Overall: 30 model requests, latency p50 4.665 s / p95 17.4994 s.
Recorder ↔ transcript cross-check: 30/30 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000301-s2a_bug_followup-deepseek-v4-baseline-rep0/`

### 20261029-000309-s2a_bug_followup-deepseek-v4-baseline-rep1 — s2a_bug_followup × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| test_calc.py::test_pct fails — pct() missing *100 | bug | completed | Verified successfully | 24.4 | 26 | 57.9 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 17.1 | 16.2 | 162.3 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:test_calc.py::test_pct fails — pct() missing *100', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:04:20.797179+00:00', 'detail': 'coder message at 2026-10-28T21:04:20.797179+00:00 inside tester interval 2026-10-28T21:03:38.416328+00:00…2026-10-28T21:04:21.927937+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:04:21.504147+00:00', 'detail': 'coder message at 2026-10-28T21:04:21.504147+00:00 inside tester interval 2026-10-28T21:03:38.416328+00:00…2026-10-28T21:04:21.927937+00:00'}

Bug round-trips:

- `ae9ccec1` test_calc.py::test_pct fails — pct() missing *100 (activated 2026-10-28T21:04:28.859094+00:00)
- `ccd46edf` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:05:22.458392+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 32 | 152.536 | 3.937 | 7.9641 | 140842 | 5194 |

Overall: 32 model requests, latency p50 3.937 s / p95 7.9641 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000309-s2a_bug_followup-deepseek-v4-baseline-rep1/`

### 20261029-000336-s2a_bug_followup-deepseek-v4-baseline-rep2 — s2a_bug_followup × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 37 | 22.3 | 217.3 |
| pct() in calc.py is missing * 100 — full pytest red | bug | completed | Verified successfully | 17.5 | 24.9 | 49 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:05:28.482146+00:00', 'detail': 'coder message at 2026-10-28T21:05:28.482146+00:00 inside tester interval 2026-10-28T21:04:20.567813+00:00…2026-10-28T21:05:28.593559+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() in calc.py is missing * 100 — full pytest red', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:05:28.057951+00:00', 'detail': 'coder message at 2026-10-28T21:05:28.057951+00:00 inside tester interval 2026-10-28T21:04:20.567813+00:00…2026-10-28T21:05:28.593559+00:00'}

Bug round-trips:

- `a4bec92b` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:06:18.950712+00:00)
- `c20d55c2` pct() in calc.py is missing * 100 — full pytest red (activated 2026-10-28T21:05:35.234397+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 35 | 202.504 | 3.67 | 14.7816 | 131435 | 7291 |

Overall: 35 model requests, latency p50 3.67 s / p95 14.7816 s.
Recorder ↔ transcript cross-check: 35/35 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000336-s2a_bug_followup-deepseek-v4-baseline-rep2/`

### 20261029-000601-s2a_bug_followup-deepseek-v4-baseline-rep3 — s2a_bug_followup × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 27.1 | 25.7 | 200.2 |
| pct() missing `* 100` — test_pct fails | bug | completed | Verified successfully | 15.2 | 34.1 | 52.2 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:07:32.028213+00:00', 'detail': 'coder message at 2026-10-28T21:07:32.028213+00:00 inside tester interval 2026-10-28T21:06:32.896118+00:00…2026-10-28T21:07:38.082759+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() missing `* 100` — test_pct fails', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:07:37.532993+00:00', 'detail': 'coder message at 2026-10-28T21:07:37.532993+00:00 inside tester interval 2026-10-28T21:06:32.896118+00:00…2026-10-28T21:07:38.082759+00:00'}

Bug round-trips:

- `a6740408` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:08:37.191578+00:00)
- `fdabbd45` pct() missing `* 100` — test_pct fails (activated 2026-10-28T21:07:42.952945+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 33 | 183.334 | 4.1 | 10.7468 | 149087 | 7015 |

Overall: 33 model requests, latency p50 4.1 s / p95 10.7468 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000601-s2a_bug_followup-deepseek-v4-baseline-rep3/`

### 20261029-000632-s2a_bug_followup-deepseek-v4-baseline-rep4 — s2a_bug_followup × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 15.1 | 20.7 | 155.7 |
| pct() returns a/b without *100 (test_pct fails) | bug | completed | Verified successfully | 16.7 | 20.2 | 55.6 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:07:52.614362+00:00', 'detail': 'coder message at 2026-10-28T21:07:52.614362+00:00 inside tester interval 2026-10-28T21:07:01.098934+00:00…2026-10-28T21:07:52.675870+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() returns a/b without *100 (test_pct fails)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:07:38.332887+00:00', 'detail': 'coder message at 2026-10-28T21:07:38.332887+00:00 inside tester interval 2026-10-28T21:07:01.098934+00:00…2026-10-28T21:07:52.675870+00:00'}

Bug round-trips:

- `0c2de832` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:08:37.309965+00:00)
- `6bd9d50d` pct() returns a/b without *100 (test_pct fails) (activated 2026-10-28T21:07:59.564115+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 28 | 148.512 | 3.4885 | 13.4128 | 98057 | 5677 |

Overall: 28 model requests, latency p50 3.4885 s / p95 13.4128 s.
Recorder ↔ transcript cross-check: 28/28 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000632-s2a_bug_followup-deepseek-v4-baseline-rep4/`

### 20261029-000722-s2a_bug_followup-deepseek-v4-baseline-rep5 — s2a_bug_followup × deepseek-v4-baseline

Reason: `scenario failure: task 'test_pct fails — pct() missing *100 (out of scope follow-up)' (a20d27c2) awaits clarification but no scenario answer matches: 'Should I fix the pct() bug (add `* 100`) now so that `pytest -q` is fully green, or leave pct() untouched as the separate follow-up task that your message describes as out of scope?'`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | testing | — | 13.9 | — | — |
| test_pct fails — pct() missing *100 (out of scope follow-up) | bug | clarification | — | 22.6 | — | — |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:08:34.386810+00:00', 'detail': 'coder message at 2026-10-28T21:08:34.386810+00:00 inside tester interval 2026-10-28T21:07:56.573029+00:00…2026-10-28T21:08:36.440740+00:00'}
- {'source': 'transcripts', 'coder': 'bug:test_pct fails — pct() missing *100 (out of scope follow-up)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:08:33.935980+00:00', 'detail': 'coder message at 2026-10-28T21:08:33.935980+00:00 inside tester interval 2026-10-28T21:07:56.573029+00:00…2026-10-28T21:08:36.440740+00:00'}

Bug round-trips:

- `8c208a65` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:09:09.198653+00:00)
- `a20d27c2` test_pct fails — pct() missing *100 (out of scope follow-up) (activated 2026-10-28T21:08:44.047416+00:00)

User-simulator interventions: 1 (failure: 1, followup: 1, start: 1)
- SIM FAILURE: task 'test_pct fails — pct() missing *100 (out of scope follow-up)' (a20d27c2) awaits clarification but no scenario answer matches: 'Should I fix the pct() bug (add `* 100`) now so that `pytest -q` is fully green, or leave pct() untouched as the separate follow-up task that your message describes as out of scope?'

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 19 | 108.019 | 3.093 | 19.8912 | 70211 | 4402 |

Overall: 19 model requests, latency p50 3.093 s / p95 19.8912 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000722-s2a_bug_followup-deepseek-v4-baseline-rep5/`

### 20261029-000917-s2a_bug_followup-deepseek-v4-baseline-rep6 — s2a_bug_followup × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 33.1 | 15.1 | 133.6 |
| pct() missing *100 causes full pytest failure | bug | completed | Verified successfully | 13.4 | 22.7 | 41 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:10:05.207788+00:00', 'detail': 'coder message at 2026-10-28T21:10:05.207788+00:00 inside tester interval 2026-10-28T21:09:40.396394+00:00…2026-10-28T21:10:05.529070+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() missing *100 causes full pytest failure', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:10:05.007473+00:00', 'detail': 'coder message at 2026-10-28T21:10:05.007473+00:00 inside tester interval 2026-10-28T21:09:40.396394+00:00…2026-10-28T21:10:05.529070+00:00'}

Bug round-trips:

- `2df3b8b8` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:10:50.193909+00:00)
- `af165ae1` pct() missing *100 causes full pytest failure (activated 2026-10-28T21:10:10.649044+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 30 | 123.145 | 3.3545 | 7.9428 | 108297 | 5101 |

Overall: 30 model requests, latency p50 3.3545 s / p95 7.9428 s.
Recorder ↔ transcript cross-check: 30/30 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000917-s2a_bug_followup-deepseek-v4-baseline-rep6/`

### 20261029-000928-s2a_bug_followup-deepseek-v4-baseline-rep7 — s2a_bug_followup × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 17.1 | 15.1 | 189.2 |
| test_pct fails: pct() missing *100 (0.25 instead of 25.0) | bug | completed | Verified successfully | 10.7 | 25.2 | 41.1 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:test_pct fails: pct() missing *100 (0.25 instead of 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:11:24.819034+00:00', 'detail': 'coder message at 2026-10-28T21:11:24.819034+00:00 inside tester interval 2026-10-28T21:09:53.499577+00:00…2026-10-28T21:11:25.440092+00:00'}

Bug round-trips:

- `28db516f` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:12:10.145518+00:00)
- `96040d16` test_pct fails: pct() missing *100 (0.25 instead of 25.0) (activated 2026-10-28T21:11:31.000884+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 28 | 179.384 | 3.8775 | 11.7054 | 98841 | 7698 |

Overall: 28 model requests, latency p50 3.8775 s / p95 11.7054 s.
Recorder ↔ transcript cross-check: 27/28 transcript responses matched, 1 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-000928-s2a_bug_followup-deepseek-v4-baseline-rep7/`

### 20261029-000933-s2a_bug_followup-deepseek-v4-baseline-rep8 — s2a_bug_followup × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 15.2 | 19.4 | 164.8 |
| test_calc.py::test_pct fails — pct() missing * 100 (pre-existing seed bug) | bug | completed | Verified successfully | 12.5 | 23.4 | 35.8 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:11:04.740163+00:00', 'detail': 'coder message at 2026-10-28T21:11:04.740163+00:00 inside tester interval 2026-10-28T21:09:57.256410+00:00…2026-10-28T21:11:04.787545+00:00'}
- {'source': 'transcripts', 'coder': 'bug:test_calc.py::test_pct fails — pct() missing * 100 (pre-existing seed bug)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:11:04.038936+00:00', 'detail': 'coder message at 2026-10-28T21:11:04.038936+00:00 inside tester interval 2026-10-28T21:09:57.256410+00:00…2026-10-28T21:11:04.787545+00:00'}

Bug round-trips:

- `002009e5` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:11:48.946574+00:00)
- `2fda78a3` test_calc.py::test_pct fails — pct() missing * 100 (pre-existing seed bug) (activated 2026-10-28T21:11:10.597030+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 28 | 152.101 | 3.7875 | 16.9842 | 100471 | 6363 |

Overall: 28 model requests, latency p50 3.7875 s / p95 16.9842 s.
Recorder ↔ transcript cross-check: 28/28 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000933-s2a_bug_followup-deepseek-v4-baseline-rep8/`

### 20261029-001145-s2a_bug_followup-deepseek-v4-baseline-rep9 — s2a_bug_followup × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 25.7 | 17.9 | 188.5 |
| test_pct fails: pct() missing *100 (out of task scope) | bug | completed | Verified successfully | 22.5 | 31.2 | 72.4 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:13:15.259526+00:00', 'detail': 'coder message at 2026-10-28T21:13:15.259526+00:00 inside tester interval 2026-10-28T21:12:12.422844+00:00…2026-10-28T21:13:15.518148+00:00'}
- {'source': 'transcripts', 'coder': 'bug:test_pct fails: pct() missing *100 (out of task scope)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:13:02.465908+00:00', 'detail': 'coder message at 2026-10-28T21:13:02.465908+00:00 inside tester interval 2026-10-28T21:12:12.422844+00:00…2026-10-28T21:13:15.518148+00:00'}

Bug round-trips:

- `7f369e84` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:14:18.035744+00:00)
- `aab60ecd` test_pct fails: pct() missing *100 (out of task scope) (activated 2026-10-28T21:13:21.771340+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 33 | 176.058 | 4.129 | 9.4376 | 123894 | 7461 |

Overall: 33 model requests, latency p50 4.129 s / p95 9.4376 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001145-s2a_bug_followup-deepseek-v4-baseline-rep9/`

### 20261029-000026-s2a_bug_followup-glm-5.3-baseline-rep0 — s2a_bug_followup × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() в calc.py возвращает a/b вместо a/b*100 (test_pct падает) | bug | completed | Verified successfully | 5.4 | 5.1 | 11.4 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.4 | 8.5 | 42.8 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() в calc.py возвращает a/b вместо a/b*100 (test_pct падает)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:00:48.934340+00:00', 'detail': 'coder message at 2026-10-28T21:00:48.934340+00:00 inside tester interval 2026-10-28T21:00:41.068850+00:00…2026-10-28T21:00:49.574451+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:00:48.046220+00:00', 'detail': 'coder message at 2026-10-28T21:00:48.046220+00:00 inside tester interval 2026-10-28T21:00:41.068850+00:00…2026-10-28T21:00:49.574451+00:00'}

Bug round-trips:

- `b0fd1964` pct() в calc.py возвращает a/b вместо a/b*100 (test_pct падает) (activated 2026-10-28T21:00:50.388417+00:00)
- `fc117add` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:01:01.463009+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 29 | 33 | 0.974 | 2.2984 | 95183 | 2901 |

Overall: 29 model requests, latency p50 0.974 s / p95 2.2984 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000026-s2a_bug_followup-glm-5.3-baseline-rep0/`

### 20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep1 — s2a_bug_followup × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.4 | 5.6 | 40.2 |
| calc.py: pct() возвращает a / b вместо (a / b) * 100 — test_pct падает | bug | completed | Verified successfully | 3.7 | 7 | 12.2 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:00:51.154278+00:00', 'detail': 'coder message at 2026-10-28T21:00:51.154278+00:00 inside tester interval 2026-10-28T21:00:45.304275+00:00…2026-10-28T21:00:54.143597+00:00'}
- {'source': 'transcripts', 'coder': 'bug:calc.py: pct() возвращает a / b вместо (a / b) * 100 — test_pct падает', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:00:53.180485+00:00', 'detail': 'coder message at 2026-10-28T21:00:53.180485+00:00 inside tester interval 2026-10-28T21:00:45.304275+00:00…2026-10-28T21:00:54.143597+00:00'}

Bug round-trips:

- `005bbe4b` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:01:06.254778+00:00)
- `f7734ab8` calc.py: pct() возвращает a / b вместо (a / b) * 100 — test_pct падает (activated 2026-10-28T21:00:55.092725+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 26 | 27.748 | 0.8305 | 2.0748 | 84199 | 2774 |

Overall: 26 model requests, latency p50 0.8305 s / p95 2.0748 s.
Recorder ↔ transcript cross-check: 26/26 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep1/`

### 20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep2 — s2a_bug_followup × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 5.5 | 10.8 | 47.8 |
| calc.pct() возвращает a/b вместо a/b*100 — падает test_pct | bug | completed | Verified successfully | 4.1 | 8.4 | 13.2 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:00:51.150147+00:00', 'detail': 'coder message at 2026-10-28T21:00:51.150147+00:00 inside tester interval 2026-10-28T21:00:43.151615+00:00…2026-10-28T21:00:53.172846+00:00'}
- {'source': 'transcripts', 'coder': 'bug:calc.pct() возвращает a/b вместо a/b*100 — падает test_pct', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:00:52.688600+00:00', 'detail': 'coder message at 2026-10-28T21:00:52.688600+00:00 inside tester interval 2026-10-28T21:00:43.151615+00:00…2026-10-28T21:00:53.172846+00:00'}

Bug round-trips:

- `21c01e6e` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:01:07.788438+00:00)
- `7b948365` calc.pct() возвращает a/b вместо a/b*100 — падает test_pct (activated 2026-10-28T21:00:54.501216+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 30 | 33.165 | 0.951 | 1.9223 | 100000 | 2994 |

Overall: 30 model requests, latency p50 0.951 s / p95 1.9223 s.
Recorder ↔ transcript cross-check: 30/30 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000030-s2a_bug_followup-glm-5.3-baseline-rep2/`

### 20261029-000118-s2a_bug_followup-glm-5.3-baseline-rep3 — s2a_bug_followup × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() в calc.py теряет умножение на 100 (test_pct красный) | bug | completed | Verified successfully | 3.8 | 4.7 | 9.6 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.7 | 4.4 | 32.7 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() в calc.py теряет умножение на 100 (test_pct красный)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:01:40.098219+00:00', 'detail': 'coder message at 2026-10-28T21:01:40.098219+00:00 inside tester interval 2026-10-28T21:01:33.913939+00:00…2026-10-28T21:01:40.573606+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:01:38.930971+00:00', 'detail': 'coder message at 2026-10-28T21:01:38.930971+00:00 inside tester interval 2026-10-28T21:01:33.913939+00:00…2026-10-28T21:01:40.573606+00:00'}

Bug round-trips:

- `b1366869` pct() в calc.py теряет умножение на 100 (test_pct красный) (activated 2026-10-28T21:01:41.603063+00:00)
- `fdc442fb` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:01:50.589061+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 26 | 21.839 | 0.7225 | 1.4902 | 85329 | 2595 |

Overall: 26 model requests, latency p50 0.7225 s / p95 1.4902 s.
Recorder ↔ transcript cross-check: 26/26 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000118-s2a_bug_followup-glm-5.3-baseline-rep3/`

### 20261029-000119-s2a_bug_followup-glm-5.3-baseline-rep4 — s2a_bug_followup × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.1 | 9.4 | 40.8 |
| pct() не умножает на 100 — test_pct падает (демо-дефект s2a_bug_followup) | bug | completed | Verified successfully | 4.4 | 4.2 | 9.6 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:01:41.932867+00:00', 'detail': 'coder message at 2026-10-28T21:01:41.932867+00:00 inside tester interval 2026-10-28T21:01:33.758609+00:00…2026-10-28T21:01:44.302877+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100 — test_pct падает (демо-дефект s2a_bug_followup)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:01:43.902981+00:00', 'detail': 'coder message at 2026-10-28T21:01:43.902981+00:00 inside tester interval 2026-10-28T21:01:33.758609+00:00…2026-10-28T21:01:44.302877+00:00'}

Bug round-trips:

- `57ee7a03` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:01:54.347465+00:00)
- `71e5fd99` pct() не умножает на 100 — test_pct падает (демо-дефект s2a_bug_followup) (activated 2026-10-28T21:01:45.290232+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 32 | 27.601 | 0.7255 | 1.6706 | 105130 | 2946 |

Overall: 32 model requests, latency p50 0.7255 s / p95 1.6706 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000119-s2a_bug_followup-glm-5.3-baseline-rep4/`

### 20261029-000127-s2a_bug_followup-glm-5.3-baseline-rep5 — s2a_bug_followup × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| calc.pct() missing * 100 — test_pct fails (out-of-scope defect found during task #db0f6ce7 verification) | bug | completed | Verified successfully | 3.8 | 4.9 | 9.9 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 9.2 | 5.4 | 40.4 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:calc.pct() missing * 100 — test_pct fails (out-of-scope defect found during task #db0f6ce7 verification)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:01:46.399452+00:00', 'detail': 'coder message at 2026-10-28T21:01:46.399452+00:00 inside tester interval 2026-10-28T21:01:37.795816+00:00…2026-10-28T21:01:46.885877+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:01:44.893340+00:00', 'detail': 'coder message at 2026-10-28T21:01:44.893340+00:00 inside tester interval 2026-10-28T21:01:37.795816+00:00…2026-10-28T21:01:46.885877+00:00'}

Bug round-trips:

- `0b3eaa56` calc.pct() missing * 100 — test_pct fails (out-of-scope defect found during task #db0f6ce7 verification) (activated 2026-10-28T21:01:48.049152+00:00)
- `db0f6ce7` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:01:57.286394+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 28 | 28.702 | 0.7345 | 2.6489 | 95616 | 3540 |

Overall: 28 model requests, latency p50 0.7345 s / p95 2.6489 s.
Recorder ↔ transcript cross-check: 28/28 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000127-s2a_bug_followup-glm-5.3-baseline-rep5/`

### 20261029-000201-s2a_bug_followup-glm-5.3-baseline-rep6 — s2a_bug_followup × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 5 | 5.4 | 39.4 |
| calc.py: pct() возвращает долю вместо процентов (не хватает * 100) | bug | completed | Verified successfully | 3.7 | 5.7 | 14.1 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:02:19.144453+00:00', 'detail': 'coder message at 2026-10-28T21:02:19.144453+00:00 inside tester interval 2026-10-28T21:02:14.062043+00:00…2026-10-28T21:02:24.925182+00:00'}
- {'source': 'transcripts', 'coder': 'bug:calc.py: pct() возвращает долю вместо процентов (не хватает * 100)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:02:20.386584+00:00', 'detail': 'coder message at 2026-10-28T21:02:20.386584+00:00 inside tester interval 2026-10-28T21:02:14.062043+00:00…2026-10-28T21:02:24.925182+00:00'}

Bug round-trips:

- `415d60b5` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:02:35.766728+00:00)
- `41b22713` calc.py: pct() возвращает долю вместо процентов (не хватает * 100) (activated 2026-10-28T21:02:25.391562+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 28 | 28.637 | 0.813 | 2.2392 | 92101 | 3035 |

Overall: 28 model requests, latency p50 0.813 s / p95 2.2392 s.
Recorder ↔ transcript cross-check: 28/28 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000201-s2a_bug_followup-glm-5.3-baseline-rep6/`

### 20261029-000211-s2a_bug_followup-glm-5.3-baseline-rep7 — s2a_bug_followup × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.6 | 5.9 | 42.1 |
| calc.pct() не умножает на 100 — test_pct падает | bug | completed | Verified successfully | 4.3 | 5.2 | 11.2 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:02:33.971008+00:00', 'detail': 'coder message at 2026-10-28T21:02:33.971008+00:00 inside tester interval 2026-10-28T21:02:27.760649+00:00…2026-10-28T21:02:36.375606+00:00'}
- {'source': 'transcripts', 'coder': 'bug:calc.pct() не умножает на 100 — test_pct падает', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:02:35.281548+00:00', 'detail': 'coder message at 2026-10-28T21:02:35.281548+00:00 inside tester interval 2026-10-28T21:02:27.760649+00:00…2026-10-28T21:02:36.375606+00:00'}

Bug round-trips:

- `41a975dd` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:02:47.544723+00:00)
- `bfebd275` calc.pct() не умножает на 100 — test_pct падает (activated 2026-10-28T21:02:37.407994+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 31 | 31.359 | 0.691 | 2.15 | 104348 | 2792 |

Overall: 31 model requests, latency p50 0.691 s / p95 2.15 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000211-s2a_bug_followup-glm-5.3-baseline-rep7/`

### 20261029-000214-s2a_bug_followup-glm-5.3-baseline-rep8 — s2a_bug_followup × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.2 | 9.1 | 44.6 |
| calc.pct() missing * 100 — returns a/b instead of a/b*100 | bug | completed | Verified successfully | 3.5 | 6 | 11.3 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:02:37.430133+00:00', 'detail': 'coder message at 2026-10-28T21:02:37.430133+00:00 inside tester interval 2026-10-28T21:02:31.005326+00:00…2026-10-28T21:02:39.224536+00:00'}
- {'source': 'transcripts', 'coder': 'bug:calc.pct() missing * 100 — returns a/b instead of a/b*100', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:02:38.641186+00:00', 'detail': 'coder message at 2026-10-28T21:02:38.641186+00:00 inside tester interval 2026-10-28T21:02:31.005326+00:00…2026-10-28T21:02:39.224536+00:00'}

Bug round-trips:

- `1843c975` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:02:50.863152+00:00)
- `748776d8` calc.pct() missing * 100 — returns a/b instead of a/b*100 (activated 2026-10-28T21:02:40.840254+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 30 | 32.846 | 0.7655 | 2.6512 | 101828 | 3014 |

Overall: 30 model requests, latency p50 0.7655 s / p95 2.6512 s.
Recorder ↔ transcript cross-check: 30/30 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000214-s2a_bug_followup-glm-5.3-baseline-rep8/`

### 20261029-000249-s2a_bug_followup-glm-5.3-baseline-rep9 — s2a_bug_followup × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.3 | 6 | 34.2 |
| pct() не умножает на 100 — test_pct красный | bug | completed | Verified successfully | 3.5 | 4.9 | 8.9 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:03:11.997762+00:00', 'detail': 'coder message at 2026-10-28T21:03:11.997762+00:00 inside tester interval 2026-10-28T21:03:04.662088+00:00…2026-10-28T21:03:13.156948+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100 — test_pct красный', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:03:12.730421+00:00', 'detail': 'coder message at 2026-10-28T21:03:12.730421+00:00 inside tester interval 2026-10-28T21:03:04.662088+00:00…2026-10-28T21:03:13.156948+00:00'}

Bug round-trips:

- `39ca7f7a` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:03:22.450041+00:00)
- `534bc98c` pct() не умножает на 100 — test_pct красный (activated 2026-10-28T21:03:13.596737+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 28 | 24.18 | 0.6755 | 1.8603 | 93714 | 3160 |

Overall: 28 model requests, latency p50 0.6755 s / p95 1.8603 s.
Recorder ↔ transcript cross-check: 28/28 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-000249-s2a_bug_followup-glm-5.3-baseline-rep9/`

### 20261029-001228-s2a_bug_followup-incredible-four-rep0 — s2a_bug_followup × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| test_pct падает: pct() возвращает a/b вместо a/b*100 (дефект вне объёма задачи по div()) | bug | completed | Verified successfully | 7.8 | 14.3 | 47.9 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 3.1 | 18.5 | 56.6 |

Diagnostic (§7 S6, passive): 3 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:test_pct падает: pct() возвращает a/b вместо a/b*100 (дефект вне объёма задачи по div())', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:13:04.165258+00:00', 'detail': 'coder message at 2026-10-28T21:13:04.165258+00:00 inside tester interval 2026-10-28T21:12:40.210932+00:00…2026-10-28T21:13:05.014588+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:13:04.435659+00:00', 'detail': 'coder message at 2026-10-28T21:13:04.435659+00:00 inside tester interval 2026-10-28T21:12:40.210932+00:00…2026-10-28T21:13:05.014588+00:00'}
- {'source': 'transcripts', 'coder': 'bug:test_pct падает: pct() возвращает a/b вместо a/b*100 (дефект вне объёма задачи по div())', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 1', 'at': '2026-10-28T21:13:11.987794+00:00', 'detail': 'coder message at 2026-10-28T21:13:11.987794+00:00 inside tester interval 2026-10-28T21:13:11.789968+00:00…2026-10-28T21:13:29.948789+00:00'}

Bug round-trips:

- `1bc0f4f6` test_pct падает: pct() возвращает a/b вместо a/b*100 (дефект вне объёма задачи по div()) (activated 2026-10-28T21:13:30.615694+00:00)
- `7ec6f926` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:13:08.369510+00:00)

User-simulator interventions: 2 (clarification_answer: 1, followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 13.89 | 0.767 | 1.987 | 38843 | 1569 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 19 | 52.933 | 2.027 | 6.0129 | 103864 | 9541 |

Overall: 32 model requests, latency p50 1.429 s / p95 4.9858 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001228-s2a_bug_followup-incredible-four-rep0/`

### 20261029-001247-s2a_bug_followup-incredible-four-rep1 — s2a_bug_followup × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.7 | 9.3 | 72.8 |
| pct() в calc.py не умножает на 100 — test_pct падает (pre-existing дефект, вне объёма задачи #0436c392) | bug | completed | Verified successfully | 3.7 | 15.7 | 21.4 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:13:29.287105+00:00', 'detail': 'coder message at 2026-10-28T21:13:29.287105+00:00 inside tester interval 2026-10-28T21:13:01.685354+00:00…2026-10-28T21:13:32.927562+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() в calc.py не умножает на 100 — test_pct падает (pre-existing дефект, вне объёма задачи #0436c392)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:13:32.107611+00:00', 'detail': 'coder message at 2026-10-28T21:13:32.107611+00:00 inside tester interval 2026-10-28T21:13:01.685354+00:00…2026-10-28T21:13:32.927562+00:00'}

Bug round-trips:

- `0436c392` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:13:54.592494+00:00)
- `bd4c032f` pct() в calc.py не умножает на 100 — test_pct падает (pre-existing дефект, вне объёма задачи #0436c392) (activated 2026-10-28T21:13:34.492792+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 10.469 | 0.7815 | 1.6108 | 37271 | 1173 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 17 | 51.9 | 2.141 | 6.949 | 133487 | 9091 |

Overall: 29 model requests, latency p50 1.22 s / p95 5.199 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001247-s2a_bug_followup-incredible-four-rep1/`

### 20261029-001356-s2a_bug_followup-incredible-four-rep2 — s2a_bug_followup × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 9.2 | 15.3 | 88.4 |
| pct() возвращает a/b без * 100 — test_calc.py::test_pct падает (существующий дефект вне объёма задачи div()) | bug | completed | Verified successfully | 5 | 16 | 22.4 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() возвращает a/b без * 100 — test_calc.py::test_pct падает (существующий дефект вне объёма задачи div())', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:14:43.438904+00:00', 'detail': 'coder message at 2026-10-28T21:14:43.438904+00:00 inside tester interval 2026-10-28T21:14:10.480153+00:00…2026-10-28T21:14:43.966044+00:00'}

Bug round-trips:

- `38f84e62` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:15:07.895599+00:00)
- `89be3004` pct() возвращает a/b без * 100 — test_calc.py::test_pct падает (существующий дефект вне объёма задачи div()) (activated 2026-10-28T21:14:46.034140+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 15.213 | 0.749 | 2.4715 | 48190 | 1698 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 23 | 59.045 | 1.996 | 6.8385 | 157603 | 9576 |

Overall: 38 model requests, latency p50 1.327 s / p95 5.3722 s.
Recorder ↔ transcript cross-check: 38/38 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001356-s2a_bug_followup-incredible-four-rep2/`

### 20261029-001411-s2a_bug_followup-incredible-four-rep3 — s2a_bug_followup × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| test_pct падает: pct() не умножает результат на 100 (pct(50, 200) == 0.25 вместо 25.0) | bug | completed | Verified successfully | 4.6 | 14.9 | 44.4 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 3.5 | 15.1 | 48.6 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:test_pct падает: pct() не умножает результат на 100 (pct(50, 200) == 0.25 вместо 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:14:40.182773+00:00', 'detail': 'coder message at 2026-10-28T21:14:40.182773+00:00 inside tester interval 2026-10-28T21:14:24.590189+00:00…2026-10-28T21:14:40.679135+00:00'}
- {'source': 'transcripts', 'coder': 'bug:test_pct падает: pct() не умножает результат на 100 (pct(50, 200) == 0.25 вместо 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 1', 'at': '2026-10-28T21:14:50.574143+00:00', 'detail': 'coder message at 2026-10-28T21:14:50.574143+00:00 inside tester interval 2026-10-28T21:14:50.475592+00:00…2026-10-28T21:15:05.051922+00:00'}

Bug round-trips:

- `63c3a690` test_pct падает: pct() не умножает результат на 100 (pct(50, 200) == 0.25 вместо 25.0) (activated 2026-10-28T21:15:06.088514+00:00)
- `adb92526` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:14:46.514760+00:00)

User-simulator interventions: 2 (clarification_answer: 1, followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 16.557 | 0.994 | 2.19 | 47560 | 1831 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 19 | 41.146 | 1.679 | 5.2218 | 129896 | 6451 |

Overall: 34 model requests, latency p50 1.3925 s / p95 3.7936 s.
Recorder ↔ transcript cross-check: 34/34 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001411-s2a_bug_followup-incredible-four-rep3/`

### 20261029-001506-s2a_bug_followup-incredible-four-rep4 — s2a_bug_followup × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() не умножает на 100: тест test_pct падает (assert 0.25 == 25.0) | bug | completed | Verified successfully | 3.4 | 10 | 16.1 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.3 | 24.7 | 86 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100: тест test_pct падает (assert 0.25 == 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:15:54.809155+00:00', 'detail': 'coder message at 2026-10-28T21:15:54.809155+00:00 inside tester interval 2026-10-28T21:15:22.712813+00:00…2026-10-28T21:15:56.662857+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:15:51.620208+00:00', 'detail': 'coder message at 2026-10-28T21:15:51.620208+00:00 inside tester interval 2026-10-28T21:15:22.712813+00:00…2026-10-28T21:15:56.662857+00:00'}

Bug round-trips:

- `4292f2de` pct() не умножает на 100: тест test_pct падает (assert 0.25 == 25.0) (activated 2026-10-28T21:15:57.975370+00:00)
- `c1800071` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:16:12.468385+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 10.898 | 0.588 | 1.7226 | 38281 | 1282 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 17 | 65.236 | 2.621 | 9.7698 | 140998 | 10206 |

Overall: 30 model requests, latency p50 1.2065 s / p95 7.9374 s.
Recorder ↔ transcript cross-check: 30/30 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001506-s2a_bug_followup-incredible-four-rep4/`

### 20261029-001529-s2a_bug_followup-incredible-four-rep5 — s2a_bug_followup × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() не умножает результат на 100: test_pct падает (0.25 вместо 25.0) | bug | completed | Verified successfully | 3.7 | 9.3 | 15.5 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.2 | 11.4 | 70 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает результат на 100: test_pct падает (0.25 вместо 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:16:10.667290+00:00', 'detail': 'coder message at 2026-10-28T21:16:10.667290+00:00 inside tester interval 2026-10-28T21:15:41.537912+00:00…2026-10-28T21:16:12.133379+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:16:11.242376+00:00', 'detail': 'coder message at 2026-10-28T21:16:11.242376+00:00 inside tester interval 2026-10-28T21:15:41.537912+00:00…2026-10-28T21:16:12.133379+00:00'}

Bug round-trips:

- `10113fe7` pct() не умножает результат на 100: test_pct падает (0.25 вместо 25.0) (activated 2026-10-28T21:16:13.669876+00:00)
- `d3e5887a` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:16:27.533242+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 11.924 | 0.752 | 1.8076 | 38580 | 1313 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 46.844 | 1.758 | 10.9232 | 99281 | 8384 |

Overall: 29 model requests, latency p50 1.216 s / p95 7.239 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001529-s2a_bug_followup-incredible-four-rep5/`

### 20261029-001535-s2a_bug_followup-incredible-four-rep6 — s2a_bug_followup × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 5 | 17.2 | 81.8 |
| pct() возвращает долю вместо процента: test_pct падает (assert 0.25 == 25.0) | bug | completed | Verified successfully | 3.9 | 20.1 | 26.2 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:16:09.072778+00:00', 'detail': 'coder message at 2026-10-28T21:16:09.072778+00:00 inside tester interval 2026-10-28T21:15:52.343462+00:00…2026-10-28T21:16:13.052711+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() возвращает долю вместо процента: test_pct падает (assert 0.25 == 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:16:12.538071+00:00', 'detail': 'coder message at 2026-10-28T21:16:12.538071+00:00 inside tester interval 2026-10-28T21:15:52.343462+00:00…2026-10-28T21:16:13.052711+00:00'}

Bug round-trips:

- `8d1e72ad` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:16:40.521124+00:00)
- `ae6431b0` pct() возвращает долю вместо процента: test_pct падает (assert 0.25 == 25.0) (activated 2026-10-28T21:16:15.518745+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 13.028 | 0.7655 | 2.786 | 36496 | 1111 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 21 | 53.629 | 2.945 | 4.59 | 153630 | 8226 |

Overall: 33 model requests, latency p50 1.182 s / p95 4.724 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001535-s2a_bug_followup-incredible-four-rep6/`

### 20261029-001645-s2a_bug_followup-incredible-four-rep7 — s2a_bug_followup × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() returns a/b instead of a/b*100 — test_pct fails (assert 0.25 == 25.0) | bug | completed | Verified successfully | 4.7 | 14.5 | 21.4 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 6.6 | 13.1 | 72.6 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() returns a/b instead of a/b*100 — test_pct fails (assert 0.25 == 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:17:25.062700+00:00', 'detail': 'coder message at 2026-10-28T21:17:25.062700+00:00 inside tester interval 2026-10-28T21:17:04.473749+00:00…2026-10-28T21:17:25.659157+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:17:23.134676+00:00', 'detail': 'coder message at 2026-10-28T21:17:23.134676+00:00 inside tester interval 2026-10-28T21:17:04.473749+00:00…2026-10-28T21:17:25.659157+00:00'}

Bug round-trips:

- `5dd8c032` pct() returns a/b instead of a/b*100 — test_pct fails (assert 0.25 == 25.0) (activated 2026-10-28T21:17:27.771370+00:00)
- `d343d4f0` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:17:48.100801+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 13.761 | 1.0985 | 2.1558 | 37226 | 1503 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 23 | 45.404 | 1.455 | 5.4294 | 112780 | 6892 |

Overall: 35 model requests, latency p50 1.221 s / p95 3.9738 s.
Recorder ↔ transcript cross-check: 35/35 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001645-s2a_bug_followup-incredible-four-rep7/`

### 20261029-001647-s2a_bug_followup-incredible-four-rep8 — s2a_bug_followup × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() возвращает a/b вместо a/b*100 — test_pct падает (существующий дефект, вне объёма задачи по div()) | bug | completed | Verified successfully | 4.1 | 28.5 | 35.3 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 3.4 | 14.2 | 93.6 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() возвращает a/b вместо a/b*100 — test_pct падает (существующий дефект, вне объёма задачи по div())', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:17:34.271818+00:00', 'detail': 'coder message at 2026-10-28T21:17:34.271818+00:00 inside tester interval 2026-10-28T21:17:03.013138+00:00…2026-10-28T21:17:35.969168+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:17:31.514440+00:00', 'detail': 'coder message at 2026-10-28T21:17:31.514440+00:00 inside tester interval 2026-10-28T21:17:03.013138+00:00…2026-10-28T21:17:35.969168+00:00'}

Bug round-trips:

- `01775f2e` pct() возвращает a/b вместо a/b*100 — test_pct падает (существующий дефект, вне объёма задачи по div()) (activated 2026-10-28T21:17:38.649848+00:00)
- `ffb38eae` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:18:12.145523+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 11.062 | 0.8335 | 1.7426 | 34600 | 1170 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 17 | 73.088 | 2.933 | 13.2502 | 167931 | 12083 |

Overall: 29 model requests, latency p50 1.38 s / p95 10.3778 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001647-s2a_bug_followup-incredible-four-rep8/`

### 20261029-001706-s2a_bug_followup-incredible-four-rep9 — s2a_bug_followup × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 3.9 | 8.1 | 131.8 |
| test_pct падает: pct() возвращает a/b вместо a/b*100 (дефект вне объёма задачи по div()) | bug | completed | Verified successfully | 7.5 | 11 | 81 |

Diagnostic (§7 S6, passive): 3 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:17:45.544380+00:00', 'detail': 'coder message at 2026-10-28T21:17:45.544380+00:00 inside tester interval 2026-10-28T21:17:18.338355+00:00…2026-10-28T21:17:48.505175+00:00'}
- {'source': 'transcripts', 'coder': 'bug:test_pct падает: pct() возвращает a/b вместо a/b*100 (дефект вне объёма задачи по div())', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:17:47.973854+00:00', 'detail': 'coder message at 2026-10-28T21:17:47.973854+00:00 inside tester interval 2026-10-28T21:17:18.338355+00:00…2026-10-28T21:17:48.505175+00:00'}
- {'source': 'transcripts', 'coder': 'bug:test_pct падает: pct() возвращает a/b вместо a/b*100 (дефект вне объёма задачи по div())', 'tester': 'bug:test_pct падает: pct() возвращает a/b вместо a/b*100 (дефект вне объёма задачи по div()) round 0', 'at': '2026-10-28T21:18:47.980302+00:00', 'detail': 'coder message at 2026-10-28T21:18:47.980302+00:00 inside tester interval 2026-10-28T21:17:52.999100+00:00…2026-10-28T21:18:49.629932+00:00'}

Bug round-trips:

- `7d4f9c18` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:19:10.799642+00:00)
- `da803ec0` test_pct падает: pct() возвращает a/b вместо a/b*100 (дефект вне объёма задачи по div()) (activated 2026-10-28T21:18:51.172393+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 13.261 | 0.798 | 1.7332 | 43870 | 1362 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 25 | 102.914 | 2.312 | 15.7684 | 199316 | 17208 |

Overall: 39 model requests, latency p50 1.588 s / p95 13.2743 s.
Recorder ↔ transcript cross-check: 39/39 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001706-s2a_bug_followup-incredible-four-rep9/`

### 20261029-001811-s2a_bug_followup-regular-three-rep0 — s2a_bug_followup × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() не умножает на 100 — test_pct падает (assert 0.25 == 25.0) | bug | completed | Verified successfully | 3.7 | 7 | 12.2 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 6.6 | 7.1 | 46.4 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100 — test_pct падает (assert 0.25 == 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:18:37.965205+00:00', 'detail': 'coder message at 2026-10-28T21:18:37.965205+00:00 inside tester interval 2026-10-28T21:18:25.801851+00:00…2026-10-28T21:18:38.556285+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:18:36.157062+00:00', 'detail': 'coder message at 2026-10-28T21:18:36.157062+00:00 inside tester interval 2026-10-28T21:18:25.801851+00:00…2026-10-28T21:18:38.556285+00:00'}

Bug round-trips:

- `4ff82c48` pct() не умножает на 100 — test_pct падает (assert 0.25 == 25.0) (activated 2026-10-28T21:18:40.020504+00:00)
- `e7be420f` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:18:52.198735+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 9.696 | 0.7555 | 1.3625 | 35368 | 1034 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 20 | 22.939 | 0.75 | 2.2709 | 80079 | 2611 |

Overall: 32 model requests, latency p50 0.7555 s / p95 2.1511 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001811-s2a_bug_followup-regular-three-rep0/`

### 20261029-001833-s2a_bug_followup-regular-three-rep1 — s2a_bug_followup × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() в calc.py не умножает результат на 100 — test_pct падает | bug | completed | Verified successfully | 4.7 | 6.6 | 12.7 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 5.1 | 7.2 | 40.4 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() в calc.py не умножает результат на 100 — test_pct падает', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:18:52.246244+00:00', 'detail': 'coder message at 2026-10-28T21:18:52.246244+00:00 inside tester interval 2026-10-28T21:18:44.961199+00:00…2026-10-28T21:18:52.935189+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:18:50.467358+00:00', 'detail': 'coder message at 2026-10-28T21:18:50.467358+00:00 inside tester interval 2026-10-28T21:18:44.961199+00:00…2026-10-28T21:18:52.935189+00:00'}

Bug round-trips:

- `903d5e3b` pct() в calc.py не умножает результат на 100 — test_pct падает (activated 2026-10-28T21:18:54.025723+00:00)
- `951c544e` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:19:05.971772+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 12.207 | 0.649 | 1.7906 | 39153 | 1205 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 18 | 16.552 | 0.675 | 1.9064 | 66176 | 1988 |

Overall: 31 model requests, latency p50 0.674 s / p95 2.01 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001833-s2a_bug_followup-regular-three-rep1/`

### 20261029-001909-s2a_bug_followup-regular-three-rep2 — s2a_bug_followup × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 7 | 13.4 | 50.5 |
| pct() в calc.py не умножает на 100 — test_pct падает (дефект вне объёма задачи #c396bd94) | bug | completed | Verified successfully | 4.7 | 6.2 | 12.2 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:19:29.268424+00:00', 'detail': 'coder message at 2026-10-28T21:19:29.268424+00:00 inside tester interval 2026-10-28T21:19:21.903533+00:00…2026-10-28T21:19:31.078946+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() в calc.py не умножает на 100 — test_pct падает (дефект вне объёма задачи #c396bd94)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:19:30.542222+00:00', 'detail': 'coder message at 2026-10-28T21:19:30.542222+00:00 inside tester interval 2026-10-28T21:19:21.903533+00:00…2026-10-28T21:19:31.078946+00:00'}

Bug round-trips:

- `c396bd94` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:19:43.704800+00:00)
- `d96bf633` pct() в calc.py не умножает на 100 — test_pct падает (дефект вне объёма задачи #c396bd94) (activated 2026-10-28T21:19:32.384468+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 14.167 | 0.698 | 1.8871 | 47026 | 1579 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 16 | 21.367 | 0.9215 | 3.1972 | 62291 | 2383 |

Overall: 31 model requests, latency p50 0.778 s / p95 2.5515 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001909-s2a_bug_followup-regular-three-rep2/`

### 20261029-001920-s2a_bug_followup-regular-three-rep3 — s2a_bug_followup × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.5 | 5.5 | 49.4 |
| pct() возвращает a/b вместо a/b*100 — test_pct падает | bug | completed | Verified successfully | 5.3 | 5.6 | 16.1 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:19:50.343733+00:00', 'detail': 'coder message at 2026-10-28T21:19:50.343733+00:00 inside tester interval 2026-10-28T21:19:37.338237+00:00…2026-10-28T21:19:57.159045+00:00'}
- {'source': 'transcripts', 'coder': 'bug:pct() возвращает a/b вместо a/b*100 — test_pct падает', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:19:52.220510+00:00', 'detail': 'coder message at 2026-10-28T21:19:52.220510+00:00 inside tester interval 2026-10-28T21:19:37.338237+00:00…2026-10-28T21:19:57.159045+00:00'}

Bug round-trips:

- `cc6e0ba6` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:20:08.782983+00:00)
- `dfb5937e` pct() возвращает a/b вместо a/b*100 — test_pct падает (activated 2026-10-28T21:19:57.698457+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 11.791 | 0.707 | 2.0989 | 35972 | 1119 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 19 | 20.753 | 0.676 | 2.5429 | 75918 | 2344 |

Overall: 31 model requests, latency p50 0.7 s / p95 2.679 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001920-s2a_bug_followup-regular-three-rep3/`

### 20261029-001926-s2a_bug_followup-regular-three-rep4 — s2a_bug_followup × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() не умножает на 100: test_calc.py::test_pct падает (seed-дефект вне объёма задачи #6e0726cf) | bug | completed | Verified successfully | 8.4 | 6.8 | 17.1 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.6 | 5.1 | 42.7 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100: test_calc.py::test_pct падает (seed-дефект вне объёма задачи #6e0726cf)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:19:46.364583+00:00', 'detail': 'coder message at 2026-10-28T21:19:46.364583+00:00 inside tester interval 2026-10-28T21:19:38.729636+00:00…2026-10-28T21:19:46.916099+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:19:44.497659+00:00', 'detail': 'coder message at 2026-10-28T21:19:44.497659+00:00 inside tester interval 2026-10-28T21:19:38.729636+00:00…2026-10-28T21:19:46.916099+00:00'}

Bug round-trips:

- `2c9e2996` pct() не умножает на 100: test_calc.py::test_pct падает (seed-дефект вне объёма задачи #6e0726cf) (activated 2026-10-28T21:19:48.637294+00:00)
- `6e0726cf` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:20:04.493547+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 15.195 | 0.8105 | 3.3613 | 36216 | 1169 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 15 | 15.1 | 0.757 | 2.1105 | 56539 | 2158 |

Overall: 27 model requests, latency p50 0.788 s / p95 2.1925 s.
Recorder ↔ transcript cross-check: 27/27 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-001926-s2a_bug_followup-regular-three-rep4/`

### 20261029-002006-s2a_bug_followup-regular-three-rep5 — s2a_bug_followup × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() не умножает результат на 100 — test_pct падает (assert 0.25 == 25.0) | bug | completed | Verified successfully | 3.7 | 5.1 | 10.2 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.1 | 5.1 | 42.4 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает результат на 100 — test_pct падает (assert 0.25 == 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:20:33.749007+00:00', 'detail': 'coder message at 2026-10-28T21:20:33.749007+00:00 inside tester interval 2026-10-28T21:20:18.846009+00:00…2026-10-28T21:20:34.167600+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:20:31.611392+00:00', 'detail': 'coder message at 2026-10-28T21:20:31.611392+00:00 inside tester interval 2026-10-28T21:20:18.846009+00:00…2026-10-28T21:20:34.167600+00:00'}

Bug round-trips:

- `c42732af` pct() не умножает результат на 100 — test_pct падает (assert 0.25 == 25.0) (activated 2026-10-28T21:20:35.425906+00:00)
- `d938a23b` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:20:44.646816+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 10.845 | 0.655 | 1.578 | 40112 | 1281 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 21 | 18.444 | 0.663 | 2.541 | 79902 | 2369 |

Overall: 34 model requests, latency p50 0.659 s / p95 2.3557 s.
Recorder ↔ transcript cross-check: 34/34 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002006-s2a_bug_followup-regular-three-rep5/`

### 20261029-002016-s2a_bug_followup-regular-three-rep6 — s2a_bug_followup × regular-three

Reason: `scenario failure: task 'pct() не умножает результат на 100 — test_pct падает (assert 0.25 == 25.0)' (50d53447) awaits clarification but no scenario answer matches: 'Расширяете ли вы объём и чинить ли сейчас pct() в calc.py (добавить * 100), чтобы полный pytest стал зелёным?'`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() не умножает результат на 100 — test_pct падает (assert 0.25 == 25.0) | bug | clarification | — | 2.6 | — | — |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | testing | — | 3.2 | 1.1 | — |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает результат на 100 — test_pct падает (assert 0.25 == 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:20:39.094357+00:00', 'detail': 'coder message at 2026-10-28T21:20:39.094357+00:00 inside tester interval 2026-10-28T21:20:27.980257+00:00…2026-10-28T21:20:39.660998+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:20:37.161739+00:00', 'detail': 'coder message at 2026-10-28T21:20:37.161739+00:00 inside tester interval 2026-10-28T21:20:27.980257+00:00…2026-10-28T21:20:39.660998+00:00'}

Bug round-trips:

- `50d53447` pct() не умножает результат на 100 — test_pct падает (assert 0.25 == 25.0) (activated 2026-10-28T21:20:40.833174+00:00)
- `b56bc784` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:20:43.524025+00:00)

User-simulator interventions: 1 (failure: 1, followup: 1, start: 1)
- SIM FAILURE: task 'pct() не умножает результат на 100 — test_pct падает (assert 0.25 == 25.0)' (50d53447) awaits clarification but no scenario answer matches: 'Расширяете ли вы объём и чинить ли сейчас pct() в calc.py (добавить * 100), чтобы полный pytest стал зелёным?'

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 9.158 | 0.758 | 1.7652 | 29983 | 1275 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 9.671 | 0.8625 | 2.2209 | 31766 | 1315 |

Overall: 18 model requests, latency p50 0.8425 s / p95 2.0211 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002016-s2a_bug_followup-regular-three-rep6/`

### 20261029-002021-s2a_bug_followup-regular-three-rep7 — s2a_bug_followup × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() возвращает a/b вместо a/b*100 — test_pct падает | bug | completed | Verified successfully | 4.9 | 6.2 | 12.6 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 6.1 | 6.5 | 43.5 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() возвращает a/b вместо a/b*100 — test_pct падает', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:20:42.997890+00:00', 'detail': 'coder message at 2026-10-28T21:20:42.997890+00:00 inside tester interval 2026-10-28T21:20:33.154650+00:00…2026-10-28T21:20:43.766221+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:20:41.422940+00:00', 'detail': 'coder message at 2026-10-28T21:20:41.422940+00:00 inside tester interval 2026-10-28T21:20:33.154650+00:00…2026-10-28T21:20:43.766221+00:00'}

Bug round-trips:

- `8b550af0` pct() возвращает a/b вместо a/b*100 — test_pct падает (activated 2026-10-28T21:20:44.975471+00:00)
- `ca5e6ddc` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:20:56.579717+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 13.038 | 0.78 | 1.5781 | 41876 | 1465 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 17 | 17.846 | 0.742 | 2.086 | 65251 | 2318 |

Overall: 31 model requests, latency p50 0.745 s / p95 1.8825 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002021-s2a_bug_followup-regular-three-rep7/`

### 20261029-002050-s2a_bug_followup-regular-three-rep8 — s2a_bug_followup × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() не умножает на 100: test_pct падает (assert 0.25 == 25.0) | bug | completed | Verified successfully | 4.1 | 4.5 | 10.3 |
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 4.1 | 8.6 | 41.3 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100: test_pct падает (assert 0.25 == 25.0)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:21:15.792424+00:00', 'detail': 'coder message at 2026-10-28T21:21:15.792424+00:00 inside tester interval 2026-10-28T21:21:06.802088+00:00…2026-10-28T21:21:16.261061+00:00'}
- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:21:14.150641+00:00', 'detail': 'coder message at 2026-10-28T21:21:14.150641+00:00 inside tester interval 2026-10-28T21:21:06.802088+00:00…2026-10-28T21:21:16.261061+00:00'}

Bug round-trips:

- `19c64023` pct() не умножает на 100: test_pct падает (assert 0.25 == 25.0) (activated 2026-10-28T21:21:17.925727+00:00)
- `51361a1b` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:21:27.075332+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 9.919 | 0.8135 | 1.4041 | 34946 | 1100 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 17 | 15.532 | 0.702 | 2.0632 | 63635 | 1834 |

Overall: 29 model requests, latency p50 0.757 s / p95 1.956 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002050-s2a_bug_followup-regular-three-rep8/`

### 20261029-002056-s2a_bug_followup-regular-three-rep9 — s2a_bug_followup × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | bug | completed | Verified successfully | 5.1 | 5.5 | 42.7 |
| test_pct падает: pct() не умножает на 100 (дефект вне объёма задачи про div()) | bug | completed | Verified successfully | 3.3 | 6.2 | 11.3 |

Diagnostic (§7 S6, passive): 2 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините div() (ValueError вместо ZeroDivisionError)', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:21:19.030089+00:00', 'detail': 'coder message at 2026-10-28T21:21:19.030089+00:00 inside tester interval 2026-10-28T21:21:10.898284+00:00…2026-10-28T21:21:21.311486+00:00'}
- {'source': 'transcripts', 'coder': 'bug:test_pct падает: pct() не умножает на 100 (дефект вне объёма задачи про div())', 'tester': 'bug:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:21:20.817361+00:00', 'detail': 'coder message at 2026-10-28T21:21:20.817361+00:00 inside tester interval 2026-10-28T21:21:10.898284+00:00…2026-10-28T21:21:21.311486+00:00'}

Bug round-trips:

- `77fc97c9` Почините div() (ValueError вместо ZeroDivisionError) (activated 2026-10-28T21:21:33.190210+00:00)
- `e063e62c` test_pct падает: pct() не умножает на 100 (дефект вне объёма задачи про div()) (activated 2026-10-28T21:21:22.991713+00:00)

User-simulator interventions: 1 (followup: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 12.908 | 0.655 | 1.7813 | 46039 | 1544 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 19 | 18.076 | 0.725 | 2.1208 | 73688 | 2245 |

Overall: 34 model requests, latency p50 0.7155 s / p95 2.1303 s.
Recorder ↔ transcript cross-check: 34/34 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002056-s2a_bug_followup-regular-three-rep9/`

### 20261029-002433-s2b_bug_report-deepseek-v4-baseline-rep0 — s2b_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Внеобъёмные падения: pct() без *100 и export_api() не реализован | bug | completed | Verified successfully | 18.4 | 36.6 | 64.1 |
| Реализуйте export_api() | feature | completed | Verified successfully | 13.7 | 33.5 | 169.8 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 16.1 | 38.9 | 54.2 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Внеобъёмные падения: pct() без *100 и export_api() не реализован', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:25:36.531781+00:00', 'detail': 'coder message at 2026-10-28T21:25:36.531781+00:00 inside tester interval 2026-10-28T21:25:02.345262+00:00…2026-10-28T21:25:37.320008+00:00'}

Bug round-trips:

- `163131c0` Внеобъёмные падения: pct() без *100 и export_api() не реализован (activated 2026-10-28T21:25:46.659304+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 32 | 154.628 | 4.2815 | 10.2606 | 126152 | 5594 |

Overall: 32 model requests, latency p50 4.2815 s / p95 10.2606 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002433-s2b_bug_report-deepseek-v4-baseline-rep0/`

### 20261029-002435-s2b_bug_report-deepseek-v4-baseline-rep1 — s2b_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 18.9 | 49.5 | 219.3 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 23.7 | 40.9 | 64 |
| Out-of-scope failures: test_calc.py::test_pct and test_export.py (ImportError export_api) | bug | completed | Verified successfully | 37.4 | 42 | 83.7 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Out-of-scope failures: test_calc.py::test_pct and test_export.py (ImportError export_api)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:25:46.281341+00:00', 'detail': 'coder message at 2026-10-28T21:25:46.281341+00:00 inside tester interval 2026-10-28T21:25:12.535424+00:00…2026-10-28T21:25:46.898627+00:00'}

Bug round-trips:

- `f2c2f039` Out-of-scope failures: test_calc.py::test_pct and test_export.py (ImportError export_api) (activated 2026-10-28T21:25:51.589174+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 36 | 207.09 | 4.5425 | 15.1405 | 195651 | 7023 |

Overall: 36 model requests, latency p50 4.5425 s / p95 15.1405 s.
Recorder ↔ transcript cross-check: 36/36 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002435-s2b_bug_report-deepseek-v4-baseline-rep1/`

### 20261029-002459-s2b_bug_report-deepseek-v4-baseline-rep2 — s2b_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 11.3 | 19.5 | 202.9 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 12.1 | 45.4 | 56.5 |
| Out-of-scope failures: pct() lacks *100 and export_api() not implemented | bug | completed | Verified successfully | 66.8 | 39.8 | 110.8 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Out-of-scope failures: pct() lacks *100 and export_api() not implemented', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:26:00.284266+00:00', 'detail': 'coder message at 2026-10-28T21:26:00.284266+00:00 inside tester interval 2026-10-28T21:25:21.341728+00:00…2026-10-28T21:26:01.331800+00:00'}

Bug round-trips:

- `fbb3f41e` Out-of-scope failures: pct() lacks *100 and export_api() not implemented (activated 2026-10-28T21:26:05.296839+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 32 | 185.451 | 5.4285 | 10.2711 | 225830 | 6337 |

Overall: 32 model requests, latency p50 5.4285 s / p95 10.2711 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002459-s2b_bug_report-deepseek-v4-baseline-rep2/`

### 20261029-002739-s2b_bug_report-deepseek-v4-baseline-rep3 — s2b_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 16 | 27.5 | 378.9 |
| Out-of-scope defects: test_pct (pct missing *100) and test_export (ImportError export_api) | bug | completed | Verified successfully | 234.2 | 30 | 268.8 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 16 | 44 | 59.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Out-of-scope defects: test_pct (pct missing *100) and test_export (ImportError export_api)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:28:46.677124+00:00', 'detail': 'coder message at 2026-10-28T21:28:46.677124+00:00 inside tester interval 2026-10-28T21:28:06.463340+00:00…2026-10-28T21:28:47.237683+00:00'}

Bug round-trips:

- `b84b646e` Out-of-scope defects: test_pct (pct missing *100) and test_export (ImportError export_api) (activated 2026-10-28T21:28:53.529116+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 32 | 352.55 | 4.8725 | 53.7392 | 159144 | 13800 |

Overall: 32 model requests, latency p50 4.8725 s / p95 53.7392 s.
Recorder ↔ transcript cross-check: 30/32 transcript responses matched, 2 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-002739-s2b_bug_report-deepseek-v4-baseline-rep3/`

### 20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep4 — s2b_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 11.1 | 27.4 | 202.6 |
| Out-of-scope: pct() missing *100 and export_api not implemented | bug | completed | Verified successfully | 22.9 | 73 | 100.3 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 19.3 | 41.2 | 59.8 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Out-of-scope: pct() missing *100 and export_api not implemented', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:29:37.090722+00:00', 'detail': 'coder message at 2026-10-28T21:29:37.090722+00:00 inside tester interval 2026-10-28T21:29:02.589951+00:00…2026-10-28T21:29:37.822852+00:00'}

Bug round-trips:

- `b137ae00` Out-of-scope: pct() missing *100 and export_api not implemented (activated 2026-10-28T21:29:42.181301+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 29 | 189.182 | 5.436 | 12.7988 | 114836 | 6779 |

Overall: 29 model requests, latency p50 5.436 s / p95 12.7988 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep4/`

### 20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep5 — s2b_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 10.6 | 32.6 | 188.2 |
| pct() missing *100 and export_api() not implemented (out-of-scope failures) | bug | completed | Verified successfully | 38 | 38.3 | 83.5 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 13.7 | 44.1 | 57.2 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() missing *100 and export_api() not implemented (out-of-scope failures)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:29:32.708137+00:00', 'detail': 'coder message at 2026-10-28T21:29:32.708137+00:00 inside tester interval 2026-10-28T21:28:55.861452+00:00…2026-10-28T21:29:35.217910+00:00'}

Bug round-trips:

- `597dc447` pct() missing *100 and export_api() not implemented (out-of-scope failures) (activated 2026-10-28T21:29:40.487648+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 32 | 176.227 | 5.0085 | 11.5971 | 121467 | 6169 |

Overall: 32 model requests, latency p50 5.0085 s / p95 11.5971 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002832-s2b_bug_report-deepseek-v4-baseline-rep5/`

### 20261029-003152-s2b_bug_report-deepseek-v4-baseline-rep6 — s2b_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 11.6 | 41.5 | 52.4 |
| Out-of-scope failures: test_pct (pct missing *100) and test_export (export_api ImportError) | bug | completed | Verified successfully | 45 | 39.4 | 91.8 |
| Реализуйте export_api() | feature | completed | Verified successfully | 11.3 | 24.4 | 180.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Out-of-scope failures: test_pct (pct missing *100) and test_export (export_api ImportError)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:32:50.505039+00:00', 'detail': 'coder message at 2026-10-28T21:32:50.505039+00:00 inside tester interval 2026-10-28T21:32:17.060744+00:00…2026-10-28T21:32:52.947076+00:00'}

Bug round-trips:

- `8f9c0a0f` Out-of-scope failures: test_pct (pct missing *100) and test_export (export_api ImportError) (activated 2026-10-28T21:32:58.543312+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 29 | 173.187 | 5.156 | 13.413 | 115969 | 6442 |

Overall: 29 model requests, latency p50 5.156 s / p95 13.413 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-003152-s2b_bug_report-deepseek-v4-baseline-rep6/`

### 20261029-003208-s2b_bug_report-deepseek-v4-baseline-rep7 — s2b_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 10.5 | 36.4 | 164.3 |
| Внеобъёмные падения: pct() без умножения на 100 и нереализованная export_api() | bug | completed | Verified successfully | 18 | 25.3 | 51.5 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 15.6 | 45.8 | 59 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Внеобъёмные падения: pct() без умножения на 100 и нереализованная export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:33:12.009313+00:00', 'detail': 'coder message at 2026-10-28T21:33:12.009313+00:00 inside tester interval 2026-10-28T21:32:32.040563+00:00…2026-10-28T21:33:14.374467+00:00'}

Bug round-trips:

- `46447dd0` Внеобъёмные падения: pct() без умножения на 100 и нереализованная export_api() (activated 2026-10-28T21:33:21.540849+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 32 | 153.64 | 4.193 | 8.4409 | 125411 | 5508 |

Overall: 32 model requests, latency p50 4.193 s / p95 8.4409 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-003208-s2b_bug_report-deepseek-v4-baseline-rep7/`

### 20261029-003413-s2b_bug_report-deepseek-v4-baseline-rep8 — s2b_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 40.7 | 50.8 | 228.1 |
| Out-of-scope failures: pct() lacks *100 and export_api() not implemented | bug | completed | Verified successfully | 20.9 | 43.1 | 72.2 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 13.7 | 47.8 | 60.7 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Out-of-scope failures: pct() lacks *100 and export_api() not implemented', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:35:20.646491+00:00', 'detail': 'coder message at 2026-10-28T21:35:20.646491+00:00 inside tester interval 2026-10-28T21:34:38.289527+00:00…2026-10-28T21:35:23.328477+00:00'}

Bug round-trips:

- `c453d65f` Out-of-scope failures: pct() lacks *100 and export_api() not implemented (activated 2026-10-28T21:35:29.586013+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 36 | 212.641 | 4.786 | 13.7668 | 216031 | 7837 |

Overall: 36 model requests, latency p50 4.786 s / p95 13.7668 s.
Recorder ↔ transcript cross-check: 36/36 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-003413-s2b_bug_report-deepseek-v4-baseline-rep8/`

### 20261029-003503-s2b_bug_report-deepseek-v4-baseline-rep9 — s2b_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 15.7 | 61.3 | 76.5 |
| Реализуйте export_api() | feature | completed | Verified successfully | 21.4 | 25.9 | 178.6 |
| Out-of-scope failures: test_pct (missing *100) and test_export (export_api ImportError) | bug | completed | Verified successfully | 17.7 | 27.9 | 57.2 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Out-of-scope failures: test_pct (missing *100) and test_export (export_api ImportError)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:36:17.876865+00:00', 'detail': 'coder message at 2026-10-28T21:36:17.876865+00:00 inside tester interval 2026-10-28T21:35:27.071692+00:00…2026-10-28T21:36:24.498734+00:00'}

Bug round-trips:

- `d5e4f39f` Out-of-scope failures: test_pct (missing *100) and test_export (export_api ImportError) (activated 2026-10-28T21:36:30.434052+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 32 | 164.428 | 4.197 | 10.0182 | 126278 | 5581 |

Overall: 32 model requests, latency p50 4.197 s / p95 10.0182 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-003503-s2b_bug_report-deepseek-v4-baseline-rep9/`

### 20261029-002111-s2b_bug_report-glm-5.3-baseline-rep0 — s2b_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 7.4 | 15.4 | 58.5 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 8.2 | 15.8 | 21.6 |
| Fix out-of-scope defects in seed: pct() missing *100 and export_api() not implemented | bug | completed | Verified successfully | 4.3 | 6.1 | 11.2 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Fix out-of-scope defects in seed: pct() missing *100 and export_api() not implemented', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:21:40.358797+00:00', 'detail': 'coder message at 2026-10-28T21:21:40.358797+00:00 inside tester interval 2026-10-28T21:21:27.257474+00:00…2026-10-28T21:21:40.812978+00:00'}

Bug round-trips:

- `f7e7881c` Fix out-of-scope defects in seed: pct() missing *100 and export_api() not implemented (activated 2026-10-28T21:21:41.578634+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 37 | 37.599 | 0.865 | 1.9408 | 137385 | 3906 |

Overall: 37 model requests, latency p50 0.865 s / p95 1.9408 s.
Recorder ↔ transcript cross-check: 37/37 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002111-s2b_bug_report-glm-5.3-baseline-rep0/`

### 20261029-002142-s2b_bug_report-glm-5.3-baseline-rep1 — s2b_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 8.9 | 9.2 | 55.5 |
| Внеобъёмные падения тестов: pct() не умножает на 100 и отсутствует export_api() | bug | completed | Verified successfully | 5 | 5.1 | 12.1 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 12.4 | 14.1 | 26.1 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Внеобъёмные падения тестов: pct() не умножает на 100 и отсутствует export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:22:11.747243+00:00', 'detail': 'coder message at 2026-10-28T21:22:11.747243+00:00 inside tester interval 2026-10-28T21:22:00.550718+00:00…2026-10-28T21:22:13.421432+00:00'}

Bug round-trips:

- `438f6686` Внеобъёмные падения тестов: pct() не умножает на 100 и отсутствует export_api() (activated 2026-10-28T21:22:14.129055+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 35 | 34.782 | 0.754 | 2.0866 | 130660 | 5142 |

Overall: 35 model requests, latency p50 0.754 s / p95 2.0866 s.
Recorder ↔ transcript cross-check: 35/35 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002142-s2b_bug_report-glm-5.3-baseline-rep1/`

### 20261029-002147-s2b_bug_report-glm-5.3-baseline-rep2 — s2b_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 4.5 | 7.8 | 41.4 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 4.1 | 14.1 | 16 |
| Почините pct() (нет умножения на 100) и реализуйте export_api() | bug | completed | Verified successfully | 3.8 | 6.3 | 11.1 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините pct() (нет умножения на 100) и реализуйте export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:22:09.570416+00:00', 'detail': 'coder message at 2026-10-28T21:22:09.570416+00:00 inside tester interval 2026-10-28T21:21:57.699559+00:00…2026-10-28T21:22:10.287612+00:00'}

Bug round-trips:

- `edc1a91b` Почините pct() (нет умножения на 100) и реализуйте export_api() (activated 2026-10-28T21:22:10.976245+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 33 | 25.836 | 0.742 | 1.4174 | 114719 | 3094 |

Overall: 33 model requests, latency p50 0.742 s / p95 1.4174 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002147-s2b_bug_report-glm-5.3-baseline-rep2/`

### 20261029-002219-s2b_bug_report-glm-5.3-baseline-rep3 — s2b_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините pct() (нет умножения на 100) и реализуйте export_api() | bug | completed | Verified successfully | 4.7 | 4.7 | 11.3 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 10.7 | 14.3 | 24.2 |
| Реализуйте export_api() | feature | completed | Verified successfully | 3.5 | 8.1 | 47 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините pct() (нет умножения на 100) и реализуйте export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:22:50.824791+00:00', 'detail': 'coder message at 2026-10-28T21:22:50.824791+00:00 inside tester interval 2026-10-28T21:22:39.258829+00:00…2026-10-28T21:22:52.165495+00:00'}

Bug round-trips:

- `04c152fa` Почините pct() (нет умножения на 100) и реализуйте export_api() (activated 2026-10-28T21:22:53.055736+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 33 | 27.576 | 0.674 | 1.7082 | 117516 | 3629 |

Overall: 33 model requests, latency p50 0.674 s / p95 1.7082 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002219-s2b_bug_report-glm-5.3-baseline-rep3/`

### 20261029-002236-s2b_bug_report-glm-5.3-baseline-rep4 — s2b_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 4.2 | 10 | 49.1 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 9.2 | 15.2 | 22.2 |
| Fix out-of-scope seed defects: pct() missing *100 and export_api() not implemented | bug | completed | Verified successfully | 4 | 4.8 | 9.8 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Fix out-of-scope seed defects: pct() missing *100 and export_api() not implemented', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:23:04.690019+00:00', 'detail': 'coder message at 2026-10-28T21:23:04.690019+00:00 inside tester interval 2026-10-28T21:22:51.257654+00:00…2026-10-28T21:23:05.130522+00:00'}

Bug round-trips:

- `e2bf0ce7` Fix out-of-scope seed defects: pct() missing *100 and export_api() not implemented (activated 2026-10-28T21:23:06.144070+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 33 | 29.969 | 0.801 | 1.6704 | 118176 | 3149 |

Overall: 33 model requests, latency p50 0.801 s / p95 1.6704 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002236-s2b_bug_report-glm-5.3-baseline-rep4/`

### 20261029-002246-s2b_bug_report-glm-5.3-baseline-rep5 — s2b_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 8.9 | 14.8 | 21.4 |
| Реализуйте export_api() | feature | completed | Verified successfully | 3.1 | 7.5 | 45.5 |
| Почините pct() (нет умножения на 100) и реализуйте export_api() в calc.py | bug | completed | Verified successfully | 4.7 | 5.4 | 11 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините pct() (нет умножения на 100) и реализуйте export_api() в calc.py', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:23:14.220594+00:00', 'detail': 'coder message at 2026-10-28T21:23:14.220594+00:00 inside tester interval 2026-10-28T21:23:01.543076+00:00…2026-10-28T21:23:14.630442+00:00'}

Bug round-trips:

- `e32b3cfc` Почините pct() (нет умножения на 100) и реализуйте export_api() в calc.py (activated 2026-10-28T21:23:15.529480+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 32 | 26.286 | 0.651 | 1.585 | 113754 | 3386 |

Overall: 32 model requests, latency p50 0.651 s / p95 1.585 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002246-s2b_bug_report-glm-5.3-baseline-rep5/`

### 20261029-002317-s2b_bug_report-glm-5.3-baseline-rep6 — s2b_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 3.7 | 9.4 | 43.5 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 8.2 | 12.6 | 18.9 |
| Почините pct() (нет умножения на 100) и реализуйте export_api() (ImportError) | bug | completed | Verified successfully | 3.9 | 5.4 | 10.4 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините pct() (нет умножения на 100) и реализуйте export_api() (ImportError)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:23:42.137539+00:00', 'detail': 'coder message at 2026-10-28T21:23:42.137539+00:00 inside tester interval 2026-10-28T21:23:32.303296+00:00…2026-10-28T21:23:42.774799+00:00'}

Bug round-trips:

- `d5254e2c` Почините pct() (нет умножения на 100) и реализуйте export_api() (ImportError) (activated 2026-10-28T21:23:43.648201+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 30 | 23.745 | 0.679 | 1.5325 | 105235 | 2918 |

Overall: 30 model requests, latency p50 0.679 s / p95 1.5325 s.
Recorder ↔ transcript cross-check: 30/30 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002317-s2b_bug_report-glm-5.3-baseline-rep6/`

### 20261029-002333-s2b_bug_report-glm-5.3-baseline-rep7 — s2b_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 5.4 | 8.7 | 51 |
| Fix pct() missing *100 and implement export_api() in calc.py | bug | completed | Verified successfully | 7.5 | 4.8 | 12.7 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 9 | 14.8 | 22.1 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Fix pct() missing *100 and implement export_api() in calc.py', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:24:03.928625+00:00', 'detail': 'coder message at 2026-10-28T21:24:03.928625+00:00 inside tester interval 2026-10-28T21:23:51.992801+00:00…2026-10-28T21:24:04.427361+00:00'}

Bug round-trips:

- `3a0fa36e` Fix pct() missing *100 and implement export_api() in calc.py (activated 2026-10-28T21:24:04.956307+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 33 | 27.735 | 0.716 | 1.3404 | 114468 | 3065 |

Overall: 33 model requests, latency p50 0.716 s / p95 1.3404 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002333-s2b_bug_report-glm-5.3-baseline-rep7/`

### 20261029-002339-s2b_bug_report-glm-5.3-baseline-rep8 — s2b_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 8.5 | 16 | 22.2 |
| Закрыть внеобъёмные дефекты: pct() без умножения на 100 и нереализованная export_api() | bug | completed | Verified successfully | 4.7 | 5.2 | 10.9 |
| Реализуйте export_api() | feature | completed | Verified successfully | 3 | 7.9 | 46.8 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Закрыть внеобъёмные дефекты: pct() без умножения на 100 и нереализованная export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:24:07.326074+00:00', 'detail': 'coder message at 2026-10-28T21:24:07.326074+00:00 inside tester interval 2026-10-28T21:23:53.641745+00:00…2026-10-28T21:24:07.752343+00:00'}

Bug round-trips:

- `9f7c4741` Закрыть внеобъёмные дефекты: pct() без умножения на 100 и нереализованная export_api() (activated 2026-10-28T21:24:08.846334+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 29 | 26.639 | 0.681 | 1.8784 | 106910 | 3206 |

Overall: 29 model requests, latency p50 0.681 s / p95 1.8784 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002339-s2b_bug_report-glm-5.3-baseline-rep8/`

### 20261029-002411-s2b_bug_report-glm-5.3-baseline-rep9 — s2b_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 2.9 | 9.5 | 40.9 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 5.7 | 12.9 | 18.1 |
| Почините pct() (нет умножения на 100) и реализуйте export_api() | bug | completed | Verified successfully | 3.9 | 5.6 | 10.2 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Почините pct() (нет умножения на 100) и реализуйте export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:24:33.074494+00:00', 'detail': 'coder message at 2026-10-28T21:24:33.074494+00:00 inside tester interval 2026-10-28T21:24:21.649205+00:00…2026-10-28T21:24:33.609601+00:00'}

Bug round-trips:

- `e303bbb2` Почините pct() (нет умножения на 100) и реализуйте export_api() (activated 2026-10-28T21:24:34.240262+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 31 | 23.813 | 0.648 | 1.419 | 109334 | 2843 |

Overall: 31 model requests, latency p50 0.648 s / p95 1.419 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-002411-s2b_bug_report-glm-5.3-baseline-rep9/`

### 20261029-003505-s2b_bug_report-incredible-four-rep0 — s2b_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 13.9 | 26.7 | 39.6 |
| Реализуйте export_api() | feature | completed | Verified successfully | 3.6 | 24.6 | 93.7 |
| calc: pct() не умножает на 100 и export_api() не реализована (test_pct и test_export красные) | bug | completed | Verified successfully | 5.1 | 18.6 | 27.3 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:calc: pct() не умножает на 100 и export_api() не реализована (test_pct и test_export красные)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:35:47.039904+00:00', 'detail': 'coder message at 2026-10-28T21:35:47.039904+00:00 inside tester interval 2026-10-28T21:35:25.455363+00:00…2026-10-28T21:35:50.032165+00:00'}

Bug round-trips:

- `ecbe3a08` calc: pct() не умножает на 100 и export_api() не реализована (test_pct и test_export красные) (activated 2026-10-28T21:35:51.301147+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 17.921 | 0.6875 | 3.6318 | 44462 | 1568 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 20 | 57.635 | 1.8935 | 8.6239 | 107147 | 9564 |

Overall: 34 model requests, latency p50 1.2835 s / p95 6.7531 s.
Recorder ↔ transcript cross-check: 34/34 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-003505-s2b_bug_report-incredible-four-rep0/`

### 20261029-003648-s2b_bug_report-incredible-four-rep1 — s2b_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() не умножает на 100 (test_pct падает) и export_api() не реализована (ImportError в test_export) | bug | completed | Verified successfully | 4.3 | 51.2 | 56.3 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 9.2 | 25.7 | 28.5 |
| Реализуйте export_api() | feature | completed | Verified successfully | 5.5 | 16.1 | 114.3 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100 (test_pct падает) и export_api() не реализована (ImportError в test_export)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:37:31.793178+00:00', 'detail': 'coder message at 2026-10-28T21:37:31.793178+00:00 inside tester interval 2026-10-28T21:37:08.759542+00:00…2026-10-28T21:37:32.792662+00:00'}

Bug round-trips:

- `28887b75` pct() не умножает на 100 (test_pct падает) и export_api() не реализована (ImportError в test_export) (activated 2026-10-28T21:37:34.585743+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 16 | 12.929 | 0.643 | 1.5748 | 50822 | 1529 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 21 | 82.093 | 2.325 | 12.421 | 174658 | 14921 |

Overall: 37 model requests, latency p50 1.112 s / p95 6.801 s.
Recorder ↔ transcript cross-check: 37/37 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-003648-s2b_bug_report-incredible-four-rep1/`

### 20261029-003812-s2b_bug_report-incredible-four-rep2 — s2b_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 3.7 | 25.6 | 84.4 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 9 | 29.3 | 37.2 |
| pct() не умножает на 100 и export_api() не реализована (внеобъёмные падения из seed) | bug | completed | Verified successfully | 4.7 | 10.5 | 17 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100 и export_api() не реализована (внеобъёмные падения из seed)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:38:58.347991+00:00', 'detail': 'coder message at 2026-10-28T21:38:58.347991+00:00 inside tester interval 2026-10-28T21:38:32.610823+00:00…2026-10-28T21:38:59.520286+00:00'}

Bug round-trips:

- `aa7357b6` pct() не умножает на 100 и export_api() не реализована (внеобъёмные падения из seed) (activated 2026-10-28T21:39:00.658034+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 13.23 | 0.764 | 2.178 | 46368 | 1592 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 22 | 50.784 | 1.259 | 8.6799 | 163016 | 8169 |

Overall: 36 model requests, latency p50 1.0055 s / p95 6.6205 s.
Recorder ↔ transcript cross-check: 36/36 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-003812-s2b_bug_report-incredible-four-rep2/`

### 20261029-003816-s2b_bug_report-incredible-four-rep3 — s2b_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 5.8 | 42.8 | 133.2 |
| Внеобъёмные дефекты calc.py: pct() без умножения на 100 и не реализована export_api() | bug | completed | Verified successfully | 4.5 | 36.9 | 44.8 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 10.2 | 32.3 | 41.8 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Внеобъёмные дефекты calc.py: pct() без умножения на 100 и не реализована export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:39:00.799524+00:00', 'detail': 'coder message at 2026-10-28T21:39:00.799524+00:00 inside tester interval 2026-10-28T21:38:32.805615+00:00…2026-10-28T21:39:04.168358+00:00'}

Bug round-trips:

- `a1f74ebe` Внеобъёмные дефекты calc.py: pct() без умножения на 100 и не реализована export_api() (activated 2026-10-28T21:39:05.251396+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 16 | 13.463 | 0.7275 | 1.707 | 53061 | 1520 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 26 | 100.697 | 2.491 | 7.9535 | 322737 | 16171 |

Overall: 42 model requests, latency p50 1.6 s / p95 7.0022 s.
Recorder ↔ transcript cross-check: 42/42 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-003816-s2b_bug_report-incredible-four-rep3/`

### 20261029-003858-s2b_bug_report-incredible-four-rep4 — s2b_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Внеобъёмные дефекты: pct() без умножения на 100 и не реализованная export_api() | bug | completed | Verified successfully | 6 | 26.3 | 33.9 |
| Реализуйте export_api() | feature | completed | Verified successfully | 3.1 | 31 | 95.4 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 8.2 | 19.7 | 27.3 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Внеобъёмные дефекты: pct() без умножения на 100 и не реализованная export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:39:30.082237+00:00', 'detail': 'coder message at 2026-10-28T21:39:30.082237+00:00 inside tester interval 2026-10-28T21:39:12.803672+00:00…2026-10-28T21:39:30.628476+00:00'}

Bug round-trips:

- `0b40bedf` Внеобъёмные дефекты: pct() без умножения на 100 и не реализованная export_api() (activated 2026-10-28T21:39:32.309134+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 13.527 | 0.714 | 1.8077 | 45670 | 1471 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 22 | 64.191 | 2.1055 | 7.3185 | 194236 | 9940 |

Overall: 36 model requests, latency p50 1.404 s / p95 6.4575 s.
Recorder ↔ transcript cross-check: 36/36 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-003858-s2b_bug_report-incredible-four-rep4/`

### 20261029-003949-s2b_bug_report-incredible-four-rep5 — s2b_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Внеобъёмные падения: pct() без умножения на 100 и отсутствующая export_api() | bug | completed | Verified successfully | 3.6 | 8.7 | 14.5 |
| Реализуйте export_api() | feature | completed | Verified successfully | 5.8 | 31.8 | 96.5 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 10 | 34.1 | 40.3 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Внеобъёмные падения: pct() без умножения на 100 и отсутствующая export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:40:42.256135+00:00', 'detail': 'coder message at 2026-10-28T21:40:42.256135+00:00 inside tester interval 2026-10-28T21:40:10.387851+00:00…2026-10-28T21:40:42.897902+00:00'}

Bug round-trips:

- `a09b2f79` Внеобъёмные падения: pct() без умножения на 100 и отсутствующая export_api() (activated 2026-10-28T21:40:44.887085+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 11.597 | 0.687 | 1.5377 | 48079 | 1348 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 26 | 65.982 | 1.8845 | 5.1162 | 227996 | 9667 |

Overall: 41 model requests, latency p50 1.395 s / p95 4.877 s.
Recorder ↔ transcript cross-check: 41/41 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-003949-s2b_bug_report-incredible-four-rep5/`

### 20261029-004040-s2b_bug_report-incredible-four-rep6 — s2b_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 4.9 | 28.2 | 89.2 |
| Поправить pct() (нет *100) и реализовать export_api() в calc.py | bug | completed | Verified successfully | 3.9 | 9.1 | 16.1 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 8 | 33.1 | 39.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Поправить pct() (нет *100) и реализовать export_api() в calc.py', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:41:24.682672+00:00', 'detail': 'coder message at 2026-10-28T21:41:24.682672+00:00 inside tester interval 2026-10-28T21:40:54.017351+00:00…2026-10-28T21:41:26.170434+00:00'}

Bug round-trips:

- `21efe344` Поправить pct() (нет *100) и реализовать export_api() в calc.py (activated 2026-10-28T21:41:28.242410+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 11.816 | 0.683 | 1.5995 | 44957 | 1317 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 19 | 60.447 | 1.934 | 8.3448 | 151020 | 9831 |

Overall: 33 model requests, latency p50 1.276 s / p95 6.6374 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004040-s2b_bug_report-incredible-four-rep6/`

### 20261029-004043-s2b_bug_report-incredible-four-rep7 — s2b_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Внеобъёмные падения: test_calc.py::test_pct и test_export.py (ImportError export_api) | bug | completed | Verified successfully | 4.3 | 8 | 14.8 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 7.3 | 36.8 | 42.8 |
| Реализуйте export_api() | feature | completed | Verified successfully | 3.3 | 10.8 | 72.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Внеобъёмные падения: test_calc.py::test_pct и test_export.py (ImportError export_api)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:41:29.707269+00:00', 'detail': 'coder message at 2026-10-28T21:41:29.707269+00:00 inside tester interval 2026-10-28T21:40:57.290106+00:00…2026-10-28T21:41:31.047997+00:00'}

Bug round-trips:

- `81692f74` Внеобъёмные падения: test_calc.py::test_pct и test_export.py (ImportError export_api) (activated 2026-10-28T21:41:32.854941+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 12.429 | 0.84 | 2.3813 | 38417 | 1798 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 44.601 | 2.2595 | 7.3382 | 166185 | 8202 |

Overall: 28 model requests, latency p50 1.3485 s / p95 5.7569 s.
Recorder ↔ transcript cross-check: 28/28 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004043-s2b_bug_report-incredible-four-rep7/`

### 20261029-004140-s2b_bug_report-incredible-four-rep8 — s2b_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 10.1 | 23.7 | 30.7 |
| Внеобъёмные дефекты: pct() не умножает на 100 и не реализована export_api (test_pct + test_export красные) | bug | completed | Verified successfully | 4.4 | 32.5 | 38.7 |
| Реализуйте export_api() | feature | completed | Verified successfully | 4.1 | 13 | 90.7 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Внеобъёмные дефекты: pct() не умножает на 100 и не реализована export_api (test_pct + test_export красные)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:42:21.654077+00:00', 'detail': 'coder message at 2026-10-28T21:42:21.654077+00:00 inside tester interval 2026-10-28T21:42:00.200991+00:00…2026-10-28T21:42:22.149391+00:00'}

Bug round-trips:

- `a202791d` Внеобъёмные дефекты: pct() не умножает на 100 и не реализована export_api (test_pct + test_export красные) (activated 2026-10-28T21:42:24.150567+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 14.258 | 0.7685 | 2.5267 | 44950 | 1541 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 21 | 58.53 | 1.879 | 6.409 | 159355 | 9594 |

Overall: 35 model requests, latency p50 1.26 s / p95 5.5305 s.
Recorder ↔ transcript cross-check: 35/35 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004140-s2b_bug_report-incredible-four-rep8/`

### 20261029-004205-s2b_bug_report-incredible-four-rep9 — s2b_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 9.1 | 25.4 | 33.8 |
| Реализуйте export_api() | feature | completed | Verified successfully | 5.6 | 26.9 | 87.2 |
| Известные внеобъёмные падения: pct() (нет умножения на 100) и нереализованная export_api() | bug | completed | Verified successfully | 7.2 | 10.9 | 20.1 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Известные внеобъёмные падения: pct() (нет умножения на 100) и нереализованная export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:42:43.334890+00:00', 'detail': 'coder message at 2026-10-28T21:42:43.334890+00:00 inside tester interval 2026-10-28T21:42:20.928829+00:00…2026-10-28T21:42:43.988026+00:00'}

Bug round-trips:

- `d6f6cd2c` Известные внеобъёмные падения: pct() (нет умножения на 100) и нереализованная export_api() (activated 2026-10-28T21:42:45.836492+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 18 | 17.386 | 0.7675 | 1.7497 | 58271 | 2117 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 21 | 54.777 | 1.752 | 9.955 | 127733 | 9464 |

Overall: 39 model requests, latency p50 1.079 s / p95 4.114 s.
Recorder ↔ transcript cross-check: 39/39 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004205-s2b_bug_report-incredible-four-rep9/`

### 20261029-004218-s2b_bug_report-regular-three-rep0 — s2b_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 12.9 | 15 | 25.3 |
| Реализуйте export_api() | feature | completed | Verified successfully | 7.4 | 9.5 | 54.6 |
| pct() без умножения на 100 и export_api() не реализована (внеобъёмные дефекты seed) | bug | completed | Verified successfully | 4.3 | 4.9 | 10.1 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() без умножения на 100 и export_api() не реализована (внеобъёмные дефекты seed)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:42:50.002995+00:00', 'detail': 'coder message at 2026-10-28T21:42:50.002995+00:00 inside tester interval 2026-10-28T21:42:36.909508+00:00…2026-10-28T21:42:50.420844+00:00'}

Bug round-trips:

- `b30d9512` pct() без умножения на 100 и export_api() не реализована (внеобъёмные дефекты seed) (activated 2026-10-28T21:42:51.291023+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 17.795 | 0.723 | 3.1173 | 47063 | 1598 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 18 | 15.864 | 0.7205 | 1.4224 | 69984 | 1956 |

Overall: 33 model requests, latency p50 0.723 s / p95 1.9674 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004218-s2b_bug_report-regular-three-rep0/`

### 20261029-004320-s2b_bug_report-regular-three-rep1 — s2b_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 9.8 | 15.7 | 24.7 |
| pct() lacks *100 and export_api() not implemented | bug | completed | Verified successfully | 10.8 | 6.6 | 18.4 |
| Реализуйте export_api() | feature | completed | Verified successfully | 9.4 | 7.6 | 60.8 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() lacks *100 and export_api() not implemented', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:43:53.386430+00:00', 'detail': 'coder message at 2026-10-28T21:43:53.386430+00:00 inside tester interval 2026-10-28T21:43:39.580833+00:00…2026-10-28T21:43:54.102005+00:00'}

Bug round-trips:

- `73d07d50` pct() lacks *100 and export_api() not implemented (activated 2026-10-28T21:43:54.914588+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 17 | 22.289 | 0.764 | 4.6458 | 54058 | 1592 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 17 | 15.691 | 0.855 | 1.625 | 68127 | 1772 |

Overall: 34 model requests, latency p50 0.816 s / p95 2.9849 s.
Recorder ↔ transcript cross-check: 34/34 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004320-s2b_bug_report-regular-three-rep1/`

### 20261029-004323-s2b_bug_report-regular-three-rep2 — s2b_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 10.1 | 21.7 | 26.4 |
| Реализуйте export_api() | feature | completed | Verified successfully | 3.8 | 9.4 | 58 |
| Внеобъёмные дефекты calc: pct() без *100 и отсутствует export_api() | bug | completed | Verified successfully | 5.1 | 6.5 | 13 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Внеобъёмные дефекты calc: pct() без *100 и отсутствует export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:43:59.950506+00:00', 'detail': 'coder message at 2026-10-28T21:43:59.950506+00:00 inside tester interval 2026-10-28T21:43:39.946298+00:00…2026-10-28T21:44:00.506954+00:00'}

Bug round-trips:

- `995678dd` Внеобъёмные дефекты calc: pct() без *100 и отсутствует export_api() (activated 2026-10-28T21:44:01.715809+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 12.813 | 0.761 | 1.4946 | 46527 | 1298 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 20 | 20.89 | 0.786 | 1.902 | 88881 | 2243 |

Overall: 35 model requests, latency p50 0.761 s / p95 1.776 s.
Recorder ↔ transcript cross-check: 35/35 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004323-s2b_bug_report-regular-three-rep2/`

### 20261029-004341-s2b_bug_report-regular-three-rep3 — s2b_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| test_pct падает (нет *100 в pct) и test_export падает (нет export_api) | bug | completed | Verified successfully | 4.4 | 8.5 | 14 |
| Реализуйте export_api() | feature | completed | Verified successfully | 3.8 | 7.6 | 54.4 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 14.4 | 14.4 | 26.6 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:test_pct падает (нет *100 в pct) и test_export падает (нет export_api)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:44:14.211137+00:00', 'detail': 'coder message at 2026-10-28T21:44:14.211137+00:00 inside tester interval 2026-10-28T21:44:02.890148+00:00…2026-10-28T21:44:14.566296+00:00'}

Bug round-trips:

- `571174c7` test_pct падает (нет *100 в pct) и test_export падает (нет export_api) (activated 2026-10-28T21:44:15.886522+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 18.295 | 0.785 | 3.6815 | 44399 | 1754 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 19 | 16.864 | 0.805 | 1.6533 | 78815 | 2349 |

Overall: 33 model requests, latency p50 0.805 s / p95 1.7052 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004341-s2b_bug_report-regular-three-rep3/`

### 20261029-004430-s2b_bug_report-regular-three-rep4 — s2b_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 17.8 | 9 | 68.5 |
| pct() не умножает на 100 (test_pct падает) и export_api() не реализована (test_export — ImportError) | bug | completed | Verified successfully | 4.2 | 10.5 | 15.5 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 8.9 | 17.1 | 23 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100 (test_pct падает) и export_api() не реализована (test_export — ImportError)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:45:03.182030+00:00', 'detail': 'coder message at 2026-10-28T21:45:03.182030+00:00 inside tester interval 2026-10-28T21:44:47.948763+00:00…2026-10-28T21:45:03.659793+00:00'}

Bug round-trips:

- `9b8c0351` pct() не умножает на 100 (test_pct падает) и export_api() не реализована (test_export — ImportError) (activated 2026-10-28T21:45:04.477653+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 24.679 | 0.952 | 4.5828 | 47583 | 1435 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 20 | 22.79 | 0.676 | 2.6421 | 82497 | 2219 |

Overall: 35 model requests, latency p50 0.802 s / p95 3.4276 s.
Recorder ↔ transcript cross-check: 35/35 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004430-s2b_bug_report-regular-three-rep4/`

### 20261029-004433-s2b_bug_report-regular-three-rep5 — s2b_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 7.4 | 7.7 | 50.7 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 9.1 | 13.9 | 22.2 |
| calc: pct() не умножает на 100 и отсутствует export_api (внеобъёмные дефекты сценария) | bug | completed | Verified successfully | 6.2 | 4.9 | 12.9 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:calc: pct() не умножает на 100 и отсутствует export_api (внеобъёмные дефекты сценария)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:44:59.912645+00:00', 'detail': 'coder message at 2026-10-28T21:44:59.912645+00:00 inside tester interval 2026-10-28T21:44:48.942227+00:00…2026-10-28T21:45:00.686782+00:00'}

Bug round-trips:

- `a7c86df4` calc: pct() не умножает на 100 и отсутствует export_api (внеобъёмные дефекты сценария) (activated 2026-10-28T21:45:02.028108+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 18.298 | 0.9015 | 3.3429 | 43299 | 1414 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 15 | 14.9 | 0.777 | 2.279 | 61191 | 1936 |

Overall: 29 model requests, latency p50 0.871 s / p95 2.6564 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004433-s2b_bug_report-regular-three-rep5/`

### 20261029-004443-s2b_bug_report-regular-three-rep6 — s2b_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте export_api() | feature | completed | Verified successfully | 8.5 | 10.5 | 60.1 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 9.6 | 21.3 | 23.8 |
| calc.py: pct() не умножает на 100 и отсутствует export_api() (ImportError) | bug | completed | Verified successfully | 4 | 5.7 | 14.3 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:calc.py: pct() не умножает на 100 и отсутствует export_api() (ImportError)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:45:14.238585+00:00', 'detail': 'coder message at 2026-10-28T21:45:14.238585+00:00 inside tester interval 2026-10-28T21:45:00.091706+00:00…2026-10-28T21:45:18.805411+00:00'}

Bug round-trips:

- `42e78c92` calc.py: pct() не умножает на 100 и отсутствует export_api() (ImportError) (activated 2026-10-28T21:45:19.177333+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 15.686 | 0.9345 | 2.2602 | 43856 | 1649 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 20 | 21.502 | 0.691 | 2.6229 | 82113 | 2295 |

Overall: 34 model requests, latency p50 0.789 s / p95 2.6476 s.
Recorder ↔ transcript cross-check: 34/34 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004443-s2b_bug_report-regular-three-rep6/`

### 20261029-004532-s2b_bug_report-regular-three-rep7 — s2b_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Семейные/внеобъёмные дефекты calc.py: pct() без *100 и отсутствует export_api() | bug | completed | Verified successfully | 4.8 | 5.7 | 11.9 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 6 | 26.6 | 30 |
| Реализуйте export_api() | feature | completed | Verified successfully | 6.1 | 9.1 | 59.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Семейные/внеобъёмные дефекты calc.py: pct() без *100 и отсутствует export_api()', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:46:11.631116+00:00', 'detail': 'coder message at 2026-10-28T21:46:11.631116+00:00 inside tester interval 2026-10-28T21:45:48.033834+00:00…2026-10-28T21:46:12.406582+00:00'}

Bug round-trips:

- `60ff5780` Семейные/внеобъёмные дефекты calc.py: pct() без *100 и отсутствует export_api() (activated 2026-10-28T21:46:13.397492+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 13.71 | 0.9045 | 2.637 | 36033 | 1265 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 28 | 22.743 | 0.689 | 1.7923 | 138017 | 2822 |

Overall: 40 model requests, latency p50 0.7245 s / p95 1.9466 s.
Recorder ↔ transcript cross-check: 40/40 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004532-s2b_bug_report-regular-three-rep7/`

### 20261029-004550-s2b_bug_report-regular-three-rep8 — s2b_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 10.8 | 15.6 | 23.6 |
| Реализуйте export_api() | feature | completed | Verified successfully | 5.9 | 7.5 | 51.3 |
| pct() не умножает на 100 и отсутствует export_api (test_pct и test_export красные) | bug | completed | Verified successfully | 5.1 | 5 | 11.2 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100 и отсутствует export_api (test_pct и test_export красные)', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:46:21.064946+00:00', 'detail': 'coder message at 2026-10-28T21:46:21.064946+00:00 inside tester interval 2026-10-28T21:46:08.453014+00:00…2026-10-28T21:46:21.656395+00:00'}

Bug round-trips:

- `9d2a68df` pct() не умножает на 100 и отсутствует export_api (test_pct и test_export красные) (activated 2026-10-28T21:46:22.774562+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 15.969 | 0.733 | 2.6847 | 52242 | 1659 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 17 | 15.668 | 0.813 | 1.8072 | 68588 | 2081 |

Overall: 32 model requests, latency p50 0.7765 s / p95 2.4315 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004550-s2b_bug_report-regular-three-rep8/`

### 20261029-004551-s2b_bug_report-regular-three-rep9 — s2b_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| pct() не умножает на 100 и export_api() не реализована в calc.py | bug | completed | Verified successfully | 4.9 | 6.5 | 12.8 |
| Реализуйте export_api() | feature | completed | Verified successfully | 6.5 | 8.2 | 52.2 |
| Почините div() (ValueError вместо ZeroDivisionError) | feature | completed | Verified successfully | 8.8 | 15.9 | 22.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:pct() не умножает на 100 и export_api() не реализована в calc.py', 'tester': 'feature:Почините div() (ValueError вместо ZeroDivisionError) round 0', 'at': '2026-10-28T21:46:20.726579+00:00', 'detail': 'coder message at 2026-10-28T21:46:20.726579+00:00 inside tester interval 2026-10-28T21:46:08.789238+00:00…2026-10-28T21:46:21.156516+00:00'}

Bug round-trips:

- `01d1e9f0` pct() не умножает на 100 и export_api() не реализована в calc.py (activated 2026-10-28T21:46:22.436402+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 16.186 | 0.86 | 2.2647 | 47300 | 1648 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 19 | 16.328 | 0.739 | 1.6985 | 75066 | 2170 |

Overall: 34 model requests, latency p50 0.79 s / p95 1.7197 s.
Recorder ↔ transcript cross-check: 34/34 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-004551-s2b_bug_report-regular-three-rep9/`

### 20261029-004954-s3_compaction_coder-deepseek-v4-baseline-rep0 — s3_compaction_coder × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 178 | 35 | 212.2 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:52:44.949261+00:00 | 81 | — | 4038 | — | 2181 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 41 | 209.447 | 3.383 | 17.183 | 211369 | 8645 |

Overall: 41 model requests, latency p50 3.383 s / p95 17.183 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 30 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004954-s3_compaction_coder-deepseek-v4-baseline-rep0/`

### 20261029-005005-s3_compaction_coder-deepseek-v4-baseline-rep1 — s3_compaction_coder × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 278.5 | 23.8 | 301.9 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:54:01.002429+00:00 | 81 | — | 4378 | — | 3893 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 47 | 298.975 | 2.863 | 32.3076 | 250432 | 12408 |

Overall: 47 model requests, latency p50 2.863 s / p95 32.3076 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 31 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-005005-s3_compaction_coder-deepseek-v4-baseline-rep1/`

### 20261029-005049-s3_compaction_coder-deepseek-v4-baseline-rep2 — s3_compaction_coder × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 206.5 | 21.5 | 227.2 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:54:19.851188+00:00 | 80 | — | — | — | 2720 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 29 | 226.19 | 3.832 | 29.1408 | 149679 | 9679 |

Overall: 29 model requests, latency p50 3.832 s / p95 29.1408 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 24 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-005049-s3_compaction_coder-deepseek-v4-baseline-rep2/`

### 20261029-005340-s3_compaction_coder-deepseek-v4-baseline-rep3 — s3_compaction_coder × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 220.3 | 23.2 | 242.9 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:57:10.538976+00:00 | 81 | — | 4036 | — | 3009 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 49 | 239.574 | 2.562 | 18.7374 | 259277 | 9750 |

Overall: 49 model requests, latency p50 2.562 s / p95 18.7374 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 38 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-005340-s3_compaction_coder-deepseek-v4-baseline-rep3/`

### 20261029-005446-s3_compaction_coder-deepseek-v4-baseline-rep4 — s3_compaction_coder × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 153.1 | 35 | 183.8 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:56:57.635704+00:00 | 81 | — | 4340 | — | 4021 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 39 | 184.799 | 2.64 | 10.5927 | 205161 | 7295 |

Overall: 39 model requests, latency p50 2.64 s / p95 10.5927 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 22 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-005446-s3_compaction_coder-deepseek-v4-baseline-rep4/`

### 20261029-005517-s3_compaction_coder-deepseek-v4-baseline-rep5 — s3_compaction_coder × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 259 | 25.9 | 283.2 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:59:23.792798+00:00 | 85 | — | 4380 | — | 3273 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 43 | 279.143 | 2.639 | 32.7356 | 228870 | 11336 |

Overall: 43 model requests, latency p50 2.639 s / p95 32.7356 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 35 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-005517-s3_compaction_coder-deepseek-v4-baseline-rep5/`

### 20261029-005756-s3_compaction_coder-deepseek-v4-baseline-rep6 — s3_compaction_coder × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 158.6 | 43.3 | 201.2 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:00:05.245995+00:00 | 81 | — | 3807 | — | 2400 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 43 | 199.91 | 2.881 | 9.5539 | 224490 | 7370 |

Overall: 43 model requests, latency p50 2.881 s / p95 9.5539 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 26 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-005756-s3_compaction_coder-deepseek-v4-baseline-rep6/`

### 20261029-005807-s3_compaction_coder-deepseek-v4-baseline-rep7 — s3_compaction_coder × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 144.5 | 21.9 | 165.7 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:00:00.324357+00:00 | 81 | — | 3955 | — | 2836 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 36 | 165.588 | 2.843 | 13.4598 | 184547 | 6264 |

Overall: 36 model requests, latency p50 2.843 s / p95 13.4598 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 19 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-005807-s3_compaction_coder-deepseek-v4-baseline-rep7/`

### 20261029-010012-s3_compaction_coder-deepseek-v4-baseline-rep8 — s3_compaction_coder × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 175.1 | 43.4 | 216.4 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:02:43.400952+00:00 | 80 | — | 3881 | — | 2638 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 38 | 212.89 | 3.1415 | 12.7753 | 193629 | 7459 |

Overall: 38 model requests, latency p50 3.1415 s / p95 12.7753 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 21 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010012-s3_compaction_coder-deepseek-v4-baseline-rep8/`

### 20261029-010102-s3_compaction_coder-deepseek-v4-baseline-rep9 — s3_compaction_coder × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 188.4 | 27.1 | 214.6 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:03:49.156646+00:00 | 80 | — | 4084 | — | 3247 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 35 | 214.488 | 3.338 | 21.5204 | 180942 | 7817 |

Overall: 35 model requests, latency p50 3.338 s / p95 21.5204 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 21 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010102-s3_compaction_coder-deepseek-v4-baseline-rep9/`

### 20261029-004642-s3_compaction_coder-glm-5.3-baseline-rep0 — s3_compaction_coder × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 48 | 13 | 60.6 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:47:22.308207+00:00 | 81 | — | 4265 | — | 4388 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 54 | 55.479 | 0.6805 | 2.8319 | 274463 | 5253 |

Overall: 54 model requests, latency p50 0.6805 s / p95 2.8319 s.
Recorder ↔ transcript cross-check: 24/24 transcript responses matched, 30 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004642-s3_compaction_coder-glm-5.3-baseline-rep0/`

### 20261029-004649-s3_compaction_coder-glm-5.3-baseline-rep1 — s3_compaction_coder × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 44.6 | 8.6 | 52.7 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:47:22.515917+00:00 | 81 | — | 4087 | — | 3282 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 47 | 49.938 | 0.801 | 2.264 | 252371 | 5272 |

Overall: 47 model requests, latency p50 0.801 s / p95 2.264 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 27 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004649-s3_compaction_coder-glm-5.3-baseline-rep1/`

### 20261029-004652-s3_compaction_coder-glm-5.3-baseline-rep2 — s3_compaction_coder × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 44.4 | 12.3 | 56 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:47:25.127957+00:00 | 80 | — | 3955 | — | 3287 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 62 | 52.5 | 0.696 | 1.5628 | 316214 | 4679 |

Overall: 62 model requests, latency p50 0.696 s / p95 1.5628 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 33 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004652-s3_compaction_coder-glm-5.3-baseline-rep2/`

### 20261029-004750-s3_compaction_coder-glm-5.3-baseline-rep3 — s3_compaction_coder × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 41.2 | 8.6 | 49.4 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:48:29.985665+00:00 | 80 | — | 4171 | — | 3820 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 44 | 45.19 | 0.7805 | 1.8091 | 230920 | 5090 |

Overall: 44 model requests, latency p50 0.7805 s / p95 1.8091 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 29 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004750-s3_compaction_coder-glm-5.3-baseline-rep3/`

### 20261029-004753-s3_compaction_coder-glm-5.3-baseline-rep4 — s3_compaction_coder × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 37.7 | 8 | 45.3 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:48:29.893441+00:00 | 80 | — | 4132 | — | 3633 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 42 | 41.882 | 0.7385 | 2.2287 | 213158 | 4325 |

Overall: 42 model requests, latency p50 0.7385 s / p95 2.2287 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 29 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004753-s3_compaction_coder-glm-5.3-baseline-rep4/`

### 20261029-004756-s3_compaction_coder-glm-5.3-baseline-rep5 — s3_compaction_coder × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 38.8 | 10.1 | 48.5 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:48:32.376549+00:00 | 82 | — | 4225 | — | 4095 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 41 | 44.526 | 0.839 | 2.147 | 213663 | 5298 |

Overall: 41 model requests, latency p50 0.839 s / p95 2.147 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 27 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004756-s3_compaction_coder-glm-5.3-baseline-rep5/`

### 20261029-004846-s3_compaction_coder-glm-5.3-baseline-rep6 — s3_compaction_coder × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 54.2 | 6.6 | 60.2 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:49:44.812092+00:00 | 82 | — | — | — | 2844 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 64 | 55.532 | 0.6365 | 2.0547 | 338576 | 6506 |

Overall: 64 model requests, latency p50 0.6365 s / p95 2.0547 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 59 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004846-s3_compaction_coder-glm-5.3-baseline-rep6/`

### 20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep7 — s3_compaction_coder × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 54.5 | 7.1 | 61 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:49:46.167513+00:00 | 81 | — | 4357 | — | 3757 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 55 | 57.59 | 0.66 | 3.0849 | 295642 | 7209 |

Overall: 55 model requests, latency p50 0.66 s / p95 3.0849 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 40 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep7/`

### 20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep8 — s3_compaction_coder × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 39.4 | 8.8 | 47.7 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:49:33.320144+00:00 | 80 | — | 4025 | — | 3415 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 42 | 43.765 | 0.7735 | 2.7988 | 213314 | 4686 |

Overall: 42 model requests, latency p50 0.7735 s / p95 2.7988 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 28 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004852-s3_compaction_coder-glm-5.3-baseline-rep8/`

### 20261029-004951-s3_compaction_coder-glm-5.3-baseline-rep9 — s3_compaction_coder × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 37.4 | 12.6 | 49.5 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T21:50:23.825275+00:00 | 80 | — | 4216 | — | 3865 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 48 | 45.213 | 0.7425 | 1.6123 | 253948 | 6018 |

Overall: 48 model requests, latency p50 0.7425 s / p95 1.6123 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 28 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-004951-s3_compaction_coder-glm-5.3-baseline-rep9/`

### 20261029-010132-s3_compaction_coder-incredible-four-rep0 — s3_compaction_coder × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 58.6 | 15.6 | 73.7 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:02:21.144630+00:00 | 81 | — | 3792 | — | 2310 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 45 | 39.789 | 0.75 | 1.925 | 242736 | 3073 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 2 | 14.196 | 7.098 | 7.9305 | 10024 | 6130 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 13.649 | 1.6765 | 4.9852 | 44012 | 1863 |

Overall: 53 model requests, latency p50 0.767 s / p95 3.749 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 33 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010132-s3_compaction_coder-incredible-four-rep0/`

### 20261029-010258-s3_compaction_coder-incredible-four-rep1 — s3_compaction_coder × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 64.1 | 16.1 | 79.7 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:04:05.098630+00:00 | 81 | — | 3683 | — | 2614 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 52 | 44.174 | 0.718 | 1.5266 | 285598 | 2162 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 3 | 18.375 | 6.472 | 8.1946 | 15937 | 7994 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 14.184 | 1.355 | 3.2663 | 38746 | 2132 |

Overall: 63 model requests, latency p50 0.759 s / p95 3.5052 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 46 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010258-s3_compaction_coder-incredible-four-rep1/`

### 20261029-010403-s3_compaction_coder-incredible-four-rep2 — s3_compaction_coder × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 47.5 | 23.2 | 70.2 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:04:46.437294+00:00 | 81 | — | 3708 | — | 2402 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 35 | 33.562 | 0.692 | 2.4141 | 185179 | 1998 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 2 | 12.391 | 6.1955 | 6.8061 | 10763 | 5261 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 21.664 | 2.358 | 5.9673 | 41491 | 3526 |

Overall: 44 model requests, latency p50 0.8125 s / p95 5.8885 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 28 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010403-s3_compaction_coder-incredible-four-rep2/`

### 20261029-010431-s3_compaction_coder-incredible-four-rep3 — s3_compaction_coder × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 4.7 | 10.3 | 64.6 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Измените вес термина kappa на 42 (каталог glossary/)', 'tester': 'feature:Измените вес термина kappa на 42 (каталог glossary/) round 0', 'at': '2026-10-28T22:05:22.529029+00:00', 'detail': 'coder message at 2026-10-28T22:05:22.529029+00:00 inside tester interval 2026-10-28T22:04:52.487749+00:00…2026-10-28T22:05:23.823673+00:00'}

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:04:35.416280+00:00 | — | — | 3951 | — | 2108 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 19 | 13.455 | 0.656 | 1.0402 | 98460 | 946 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 1 | 6.776 | 6.776 | 6.776 | 5544 | 2974 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 12 | 39.116 | 2.5845 | 7.2603 | 77437 | 6100 |

Overall: 32 model requests, latency p50 0.9065 s / p95 6.2469 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 16 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010431-s3_compaction_coder-incredible-four-rep3/`

### 20261029-010449-s3_compaction_coder-incredible-four-rep4 — s3_compaction_coder × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 40.2 | 22 | 61.4 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:05:29.882961+00:00 | 81 | — | 3348 | — | 1536 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 29 | 27.236 | 0.683 | 1.7044 | 149329 | 1254 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 2 | 11.272 | 5.636 | 6.1517 | 10663 | 4721 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 16.687 | 2.097 | 2.761 | 56215 | 2484 |

Overall: 40 model requests, latency p50 0.851 s / p95 5.0688 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 28 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010449-s3_compaction_coder-incredible-four-rep4/`

### 20261029-010526-s3_compaction_coder-incredible-four-rep5 — s3_compaction_coder × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 44.8 | 17.1 | 61.2 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:06:12.282414+00:00 | 80 | — | 3397 | — | 1650 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 40 | 30.723 | 0.5925 | 1.3772 | 208905 | 1441 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 2 | 11.85 | 5.925 | 6.7143 | 10600 | 5047 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 14.934 | 2.062 | 4.9308 | 28408 | 1661 |

Overall: 48 model requests, latency p50 0.6695 s / p95 4.6455 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 34 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010526-s3_compaction_coder-incredible-four-rep5/`

### 20261029-010543-s3_compaction_coder-incredible-four-rep6 — s3_compaction_coder × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 23.3 | 27.9 | 50.5 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:06:02.660067+00:00 | 80 | — | 3462 | — | 1818 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 22 | 17.567 | 0.6545 | 1.2415 | 107153 | 908 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 1 | 4.685 | 4.685 | 4.685 | 5471 | 1859 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 10 | 26.39 | 1.9665 | 5.6101 | 79534 | 3286 |

Overall: 33 model requests, latency p50 0.755 s / p95 4.5662 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 17 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010543-s3_compaction_coder-incredible-four-rep6/`

### 20261029-010558-s3_compaction_coder-incredible-four-rep7 — s3_compaction_coder × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 40.4 | 24.8 | 63.8 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:06:34.886412+00:00 | 80 | — | 3629 | — | 1973 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 33 | 25.235 | 0.675 | 1.2418 | 160261 | 1594 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 2 | 13.367 | 6.6835 | 8.7368 | 10536 | 3798 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 20.33 | 3.221 | 5.8502 | 55991 | 3353 |

Overall: 41 model requests, latency p50 0.736 s / p95 4.816 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 26 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010558-s3_compaction_coder-incredible-four-rep7/`

### 20261029-010640-s3_compaction_coder-incredible-four-rep8 — s3_compaction_coder × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 40.2 | 23.3 | 62.7 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:07:22.907122+00:00 | 80 | — | 3501 | — | 1700 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 29 | 25.328 | 0.795 | 1.424 | 141041 | 1319 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 2 | 13.447 | 6.7235 | 7.1074 | 10471 | 5459 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 20.676 | 1.627 | 4.809 | 61326 | 3260 |

Overall: 40 model requests, latency p50 0.865 s / p95 5.1475 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 25 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010640-s3_compaction_coder-incredible-four-rep8/`

### 20261029-010642-s3_compaction_coder-incredible-four-rep9 — s3_compaction_coder × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 45.9 | 16.1 | 61.6 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:07:26.898493+00:00 | 81 | — | 3696 | — | 2569 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 38 | 33.354 | 0.752 | 1.6027 | 199569 | 1806 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 2 | 11.12 | 5.56 | 6.6193 | 10431 | 3900 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 14.12 | 1.426 | 3.3195 | 51828 | 2176 |

Overall: 47 model requests, latency p50 0.828 s / p95 3.3195 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 32 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010642-s3_compaction_coder-incredible-four-rep9/`

### 20261029-010710-s3_compaction_coder-regular-three-rep0 — s3_compaction_coder × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 34.4 | 7.5 | 41.4 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:07:38.955548+00:00 | 80 | — | 3637 | — | 2226 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 40 | 28.733 | 0.6735 | 1.1573 | 204250 | 1639 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 4.228 | 2.114 | 2.3111 | 10552 | 1375 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 4.727 | 0.765 | 1.0935 | 23618 | 546 |

Overall: 48 model requests, latency p50 0.7085 s / p95 1.5172 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 29 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010710-s3_compaction_coder-regular-three-rep0/`

### 20261029-010753-s3_compaction_coder-regular-three-rep1 — s3_compaction_coder × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 22.2 | 9.2 | 30.9 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:08:20.128603+00:00 | 80 | — | 3627 | — | 2292 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 22 | 18.202 | 0.7775 | 1.3491 | 108344 | 948 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 1 | 2.08 | 2.08 | 2.08 | 5413 | 683 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 6.235 | 0.817 | 1.8188 | 24348 | 468 |

Overall: 29 model requests, latency p50 0.798 s / p95 1.8592 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 17 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010753-s3_compaction_coder-regular-three-rep1/`

### 20261029-010755-s3_compaction_coder-regular-three-rep2 — s3_compaction_coder × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 35.8 | 8.7 | 43.9 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:08:27.831224+00:00 | 80 | — | 3903 | — | 2713 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 33 | 29.197 | 0.784 | 1.5774 | 176994 | 2299 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 5.166 | 2.583 | 2.8638 | 10525 | 1675 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 7 | 5.866 | 0.769 | 1.1649 | 31108 | 632 |

Overall: 42 model requests, latency p50 0.7855 s / p95 2.2542 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 23 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010755-s3_compaction_coder-regular-three-rep2/`

### 20261029-010759-s3_compaction_coder-regular-three-rep3 — s3_compaction_coder × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 39.8 | 23.1 | 62.4 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:08:37.448943+00:00 | 81 | — | 3795 | — | 2732 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 34 | 34.204 | 0.7505 | 2.1758 | 175426 | 2294 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 4.572 | 2.286 | 2.3823 | 10530 | 1548 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 25 | 18.196 | 0.694 | 1.252 | 193272 | 1136 |

Overall: 61 model requests, latency p50 0.717 s / p95 2.179 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 28 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010759-s3_compaction_coder-regular-three-rep3/`

### 20261029-010839-s3_compaction_coder-regular-three-rep4 — s3_compaction_coder × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 25.1 | 6.6 | 31.3 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:09:05.553592+00:00 | 81 | — | 3683 | — | 2494 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 27 | 18.834 | 0.657 | 1.0785 | 138489 | 1355 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 4.943 | 2.4715 | 2.7708 | 10584 | 1842 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.759 | 0.935 | 1.3394 | 19907 | 424 |

Overall: 34 model requests, latency p50 0.75 s / p95 1.6755 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 26 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010839-s3_compaction_coder-regular-three-rep4/`

### 20261029-010851-s3_compaction_coder-regular-three-rep5 — s3_compaction_coder × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 40 | 8.4 | 47.8 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:09:21.128248+00:00 | 80 | — | 3881 | — | 3015 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 39 | 32.721 | 0.637 | 1.4879 | 217057 | 2328 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 4.677 | 2.3385 | 2.3668 | 9964 | 1702 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 5.611 | 0.635 | 0.9596 | 33506 | 515 |

Overall: 49 model requests, latency p50 0.639 s / p95 1.8146 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 30 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010851-s3_compaction_coder-regular-three-rep5/`

### 20261029-010910-s3_compaction_coder-regular-three-rep6 — s3_compaction_coder × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 35.6 | 9.1 | 44.3 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:09:47.879093+00:00 | 81 | — | 3856 | — | 2891 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 34 | 29.214 | 0.799 | 1.3651 | 179006 | 1459 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 5.03 | 2.515 | 2.6968 | 10753 | 1780 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 9 | 6.899 | 0.578 | 1.3036 | 34225 | 645 |

Overall: 45 model requests, latency p50 0.797 s / p95 1.831 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 29 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010910-s3_compaction_coder-regular-three-rep6/`

### 20261029-010918-s3_compaction_coder-regular-three-rep7 — s3_compaction_coder × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 35.8 | 11.1 | 46.4 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:09:51.458861+00:00 | 80 | — | 3911 | — | 3409 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 32 | 29.038 | 0.9145 | 1.2683 | 169742 | 1550 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 5.332 | 2.666 | 2.702 | 10801 | 1915 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 7.248 | 0.828 | 1.333 | 38822 | 867 |

Overall: 42 model requests, latency p50 0.9145 s / p95 1.5469 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 27 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010918-s3_compaction_coder-regular-three-rep7/`

### 20261029-010946-s3_compaction_coder-regular-three-rep8 — s3_compaction_coder × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 39.2 | 10 | 48.6 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:10:20.788480+00:00 | 83 | — | 3656 | — | 1956 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 37 | 34.276 | 0.734 | 1.7016 | 194822 | 2597 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 3.625 | 1.8125 | 1.8238 | 10449 | 1215 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 6.745 | 1.1275 | 1.5975 | 26737 | 663 |

Overall: 45 model requests, latency p50 0.835 s / p95 1.82 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 30 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-010946-s3_compaction_coder-regular-three-rep8/`

### 20261029-011007-s3_compaction_coder-regular-three-rep9 — s3_compaction_coder × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Измените вес термина kappa на 42 (каталог glossary/) | feature | completed | Verified successfully | 38.1 | 13.9 | 47.3 |

Compaction savings (token estimates from response usage):

| at | trigger % | pre tokens | post tokens | saved | summary chars | prompts kept |
|---|---|---|---|---|---|---|
| 2026-10-28T22:10:42.706828+00:00 | 82 | — | 3849 | — | 2894 | 1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 35 | 31.786 | 0.759 | 1.3599 | 184574 | 2082 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 4.792 | 2.396 | 2.5427 | 10478 | 1778 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 13 | 11.475 | 0.702 | 1.62 | 61013 | 1132 |

Overall: 50 model requests, latency p50 0.763 s / p95 2.2096 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 29 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011007-s3_compaction_coder-regular-three-rep9/`

### 20261029-011528-s4_compaction_tester-deepseek-v4-baseline-rep0 — s4_compaction_tester × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 6.3 | 319.3 | 324.7 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `6d9fdb78` Почините format_report (разделитель записей) (activated 2026-10-28T22:15:31.738539+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 45 | 324.93 | 3.447 | 15.7592 | 613247 | 14866 |

Overall: 45 model requests, latency p50 3.447 s / p95 15.7592 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 35 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011528-s4_compaction_tester-deepseek-v4-baseline-rep0/`

### 20261029-011640-s4_compaction_tester-deepseek-v4-baseline-rep1 — s4_compaction_tester × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 10 | 259.9 | 268.6 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `580319ee` Почините format_report (разделитель записей) (activated 2026-10-28T22:16:48.602066+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 37 | 268.177 | 3.083 | 41.3268 | 483718 | 12120 |

Overall: 37 model requests, latency p50 3.083 s / p95 41.3268 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 27 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011640-s4_compaction_tester-deepseek-v4-baseline-rep1/`

### 20261029-011652-s4_compaction_tester-deepseek-v4-baseline-rep2 — s4_compaction_tester × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 7.9 | 276.8 | 283.7 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `3034e7b9` Почините format_report (разделитель записей) (activated 2026-10-28T22:16:55.809777+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 41 | 282.963 | 2.982 | 26.726 | 550138 | 12837 |

Overall: 41 model requests, latency p50 2.982 s / p95 26.726 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 30 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011652-s4_compaction_tester-deepseek-v4-baseline-rep2/`

### 20261029-012107-s4_compaction_tester-deepseek-v4-baseline-rep3 — s4_compaction_tester × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 10 | 202 | 211.1 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `1f7940ab` Почините format_report (разделитель записей) (activated 2026-10-28T22:21:16.871205+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 41 | 210.811 | 2.861 | 27.001 | 517788 | 9076 |

Overall: 41 model requests, latency p50 2.861 s / p95 27.001 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 30 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-012107-s4_compaction_tester-deepseek-v4-baseline-rep3/`

### 20261029-012123-s4_compaction_tester-deepseek-v4-baseline-rep4 — s4_compaction_tester × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 6.8 | 216 | 221.9 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `4b49f7b0` Почините format_report (разделитель записей) (activated 2026-10-28T22:21:27.823568+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 35 | 224.221 | 3.187 | 37.4028 | 457397 | 9692 |

Overall: 35 model requests, latency p50 3.187 s / p95 37.4028 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 26 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-012123-s4_compaction_tester-deepseek-v4-baseline-rep4/`

### 20261029-012145-s4_compaction_tester-deepseek-v4-baseline-rep5 — s4_compaction_tester × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 6.1 | 208.4 | 213.5 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `9c4b822e` Почините format_report (разделитель записей) (activated 2026-10-28T22:21:49.881557+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 35 | 213.258 | 2.691 | 33.8784 | 459991 | 9084 |

Overall: 35 model requests, latency p50 2.691 s / p95 33.8784 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 26 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-012145-s4_compaction_tester-deepseek-v4-baseline-rep5/`

### 20261029-012458-s4_compaction_tester-deepseek-v4-baseline-rep6 — s4_compaction_tester × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 157.3 | 286.9 | 443.2 |

Tester compaction threshold source: NOT tester model config — REGRESSION — threshold came from the coding model.

Bug round-trips:

- `3e6a93b0` Почините format_report (разделитель записей) (activated 2026-10-28T22:25:05.942640+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 84 | 437.702 | 2.969 | 11.3298 | 2294802 | 14091 |

Overall: 84 model requests, latency p50 2.969 s / p95 11.3298 s.
Recorder ↔ transcript cross-check: 54/54 transcript responses matched, 30 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-012458-s4_compaction_tester-deepseek-v4-baseline-rep6/`

### 20261029-012518-s4_compaction_tester-deepseek-v4-baseline-rep7 — s4_compaction_tester × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 18.5 | 329.4 | 347.1 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `177a3d32` Почините format_report (разделитель записей) (activated 2026-10-28T22:25:23.362294+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 38 | 342.185 | 3.8165 | 59.1377 | 473252 | 12868 |

Overall: 38 model requests, latency p50 3.8165 s / p95 59.1377 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 26 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-012518-s4_compaction_tester-deepseek-v4-baseline-rep7/`

### 20261029-012531-s4_compaction_tester-deepseek-v4-baseline-rep8 — s4_compaction_tester × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 9.3 | 324.6 | 330.5 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `bbecdf52` Почините format_report (разделитель записей) (activated 2026-10-28T22:25:35.135809+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 36 | 330.927 | 3.4165 | 43.7725 | 500968 | 12461 |

Overall: 36 model requests, latency p50 3.4165 s / p95 43.7725 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 25 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-012531-s4_compaction_tester-deepseek-v4-baseline-rep8/`

### 20261029-013115-s4_compaction_tester-deepseek-v4-baseline-rep9 — s4_compaction_tester × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 10.3 | 255.7 | 263.9 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `6e34fd43` Почините format_report (разделитель записей) (activated 2026-10-28T22:31:23.224633+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 38 | 264.723 | 3.516 | 30.6293 | 476444 | 11186 |

Overall: 38 model requests, latency p50 3.516 s / p95 30.6293 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 28 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-013115-s4_compaction_tester-deepseek-v4-baseline-rep9/`

### 20261029-011012-s4_compaction_tester-glm-5.3-baseline-rep0 — s4_compaction_tester × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 34.1 | 54.3 | 87.3 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `67a393f0` Почините format_report (разделитель записей) (activated 2026-10-28T22:10:18.167720+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 59 | 83.073 | 1.019 | 4.0348 | 1452350 | 7256 |

Overall: 59 model requests, latency p50 1.019 s / p95 4.0348 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 27 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011012-s4_compaction_tester-glm-5.3-baseline-rep0/`

### 20261029-011042-s4_compaction_tester-glm-5.3-baseline-rep1 — s4_compaction_tester × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 34.9 | 53.5 | 87.4 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `a1cce4df` Почините format_report (разделитель записей) (activated 2026-10-28T22:10:49.385729+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 59 | 83.528 | 1.09 | 3.6145 | 1467423 | 6755 |

Overall: 59 model requests, latency p50 1.09 s / p95 3.6145 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 28 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011042-s4_compaction_tester-glm-5.3-baseline-rep1/`

### 20261029-011109-s4_compaction_tester-glm-5.3-baseline-rep2 — s4_compaction_tester × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 34.9 | 78.1 | 111.3 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `d9aac90e` Почините format_report (разделитель записей) (activated 2026-10-28T22:11:13.450509+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 64 | 108.311 | 1.3705 | 4.4382 | 1485295 | 8032 |

Overall: 64 model requests, latency p50 1.3705 s / p95 4.4382 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 32 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011109-s4_compaction_tester-glm-5.3-baseline-rep2/`

### 20261029-011150-s4_compaction_tester-glm-5.3-baseline-rep3 — s4_compaction_tester × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 34.3 | 57.7 | 90.9 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `90e6b2e6` Почините format_report (разделитель записей) (activated 2026-10-28T22:11:57.731122+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 54 | 87.827 | 1.0595 | 5.7806 | 1344303 | 8669 |

Overall: 54 model requests, latency p50 1.0595 s / p95 5.7806 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 25 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011150-s4_compaction_tester-glm-5.3-baseline-rep3/`

### 20261029-011221-s4_compaction_tester-glm-5.3-baseline-rep4 — s4_compaction_tester × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 4.4 | 79.6 | 82.8 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `eb1c8240` Почините format_report (разделитель записей) (activated 2026-10-28T22:12:25.649304+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 36 | 80.309 | 1.817 | 6.3432 | 494450 | 7285 |

Overall: 36 model requests, latency p50 1.817 s / p95 6.3432 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 26 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011221-s4_compaction_tester-glm-5.3-baseline-rep4/`

### 20261029-011311-s4_compaction_tester-glm-5.3-baseline-rep5 — s4_compaction_tester × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 32.6 | 59.1 | 90.4 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `1b94cb3c` Почините format_report (разделитель записей) (activated 2026-10-28T22:13:18.949950+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 57 | 83.33 | 1.047 | 5.0128 | 1403166 | 8093 |

Overall: 57 model requests, latency p50 1.047 s / p95 5.0128 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 24 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011311-s4_compaction_tester-glm-5.3-baseline-rep5/`

### 20261029-011333-s4_compaction_tester-glm-5.3-baseline-rep6 — s4_compaction_tester × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 27.5 | 63.9 | 90.3 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `96803cc2` Почините format_report (разделитель записей) (activated 2026-10-28T22:13:37.509286+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 58 | 84.458 | 0.905 | 4.2194 | 1463552 | 7012 |

Overall: 58 model requests, latency p50 0.905 s / p95 4.2194 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 27 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011333-s4_compaction_tester-glm-5.3-baseline-rep6/`

### 20261029-011352-s4_compaction_tester-glm-5.3-baseline-rep7 — s4_compaction_tester × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 47.6 | 40.3 | 87.2 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `9fc5fe15` Почините format_report (разделитель записей) (activated 2026-10-28T22:13:56.710064+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 58 | 82.295 | 0.9515 | 5.0999 | 1453717 | 6839 |

Overall: 58 model requests, latency p50 0.9515 s / p95 5.0999 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 25 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011352-s4_compaction_tester-glm-5.3-baseline-rep7/`

### 20261029-011453-s4_compaction_tester-glm-5.3-baseline-rep8 — s4_compaction_tester × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 35.2 | 59.9 | 94.5 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `2033d2ff` Почините format_report (разделитель записей) (activated 2026-10-28T22:15:00.522124+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 59 | 89.768 | 1.238 | 3.7056 | 1482328 | 8204 |

Overall: 59 model requests, latency p50 1.238 s / p95 3.7056 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 28 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011453-s4_compaction_tester-glm-5.3-baseline-rep8/`

### 20261029-011513-s4_compaction_tester-glm-5.3-baseline-rep9 — s4_compaction_tester × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 32.8 | 57.5 | 89.5 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `097f9f9d` Почините format_report (разделитель записей) (activated 2026-10-28T22:15:17.187970+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 60 | 84.823 | 1.011 | 3.4586 | 1516505 | 9935 |

Overall: 60 model requests, latency p50 1.011 s / p95 3.4586 s.
Recorder ↔ transcript cross-check: 34/34 transcript responses matched, 26 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-011513-s4_compaction_tester-glm-5.3-baseline-rep9/`

### 20261029-013116-s4_compaction_tester-incredible-four-rep0 — s4_compaction_tester × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 34.3 | 241.9 | 275.2 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `6613b28d` Почините format_report (разделитель записей) (activated 2026-10-28T22:31:23.223899+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 26 | 33.077 | 1.2195 | 1.8082 | 986892 | 2090 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 71 | 183.413 | 1.718 | 6.8725 | 934204 | 23204 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 45.264 | 6.885 | 9.2525 | 148628 | 16003 |

Overall: 104 model requests, latency p50 1.4825 s / p95 7.4923 s.
Recorder ↔ transcript cross-check: 43/43 transcript responses matched, 61 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-013116-s4_compaction_tester-incredible-four-rep0/`

### 20261029-013236-s4_compaction_tester-incredible-four-rep1 — s4_compaction_tester × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 33.3 | 310.1 | 342.3 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `84ccbfa7` Почините format_report (разделитель записей) (activated 2026-10-28T22:32:45.737088+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 26 | 32.998 | 1.1605 | 1.8692 | 979689 | 1755 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 67 | 235.07 | 1.604 | 10.7813 | 931114 | 32357 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 54.828 | 5.9055 | 10.1834 | 163305 | 20866 |

Overall: 101 model requests, latency p50 1.486 s / p95 10.222 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 70 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-013236-s4_compaction_tester-incredible-four-rep1/`

### 20261029-013555-s4_compaction_tester-incredible-four-rep2 — s4_compaction_tester × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 33 | 214.2 | 246.2 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `2513ea5c` Почините format_report (разделитель записей) (activated 2026-10-28T22:36:02.643556+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 25 | 32.463 | 1.004 | 2.9376 | 893280 | 1359 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 47 | 175.066 | 1.805 | 13.8889 | 562220 | 20665 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 29.958 | 6.244 | 7.8066 | 104004 | 11784 |

Overall: 77 model requests, latency p50 1.532 s / p95 9.6362 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 46 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-013555-s4_compaction_tester-incredible-four-rep2/`

### 20261029-013603-s4_compaction_tester-incredible-four-rep3 — s4_compaction_tester × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 38.9 | 104.8 | 142.8 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `5d3cf600` Почините format_report (разделитель записей) (activated 2026-10-28T22:36:07.492386+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 26 | 37.305 | 1.14 | 3.8912 | 984420 | 1866 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 38 | 79.521 | 1.4725 | 6.6307 | 498209 | 8543 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 21.62 | 5.085 | 6.8269 | 96712 | 7791 |

Overall: 68 model requests, latency p50 1.352 s / p95 6.3437 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 37 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-013603-s4_compaction_tester-incredible-four-rep3/`

### 20261029-013835-s4_compaction_tester-incredible-four-rep4 — s4_compaction_tester × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 68.2 | 298.9 | 366.5 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `8deaacdb` Почините format_report (разделитель записей) (activated 2026-10-28T22:38:45.481218+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 25 | 79.913 | 1.053 | 14.9138 | 897289 | 1443 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 40 | 338.227 | 1.907 | 26.65 | 526177 | 10785 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 41.374 | 8.044 | 9.7638 | 109351 | 9617 |

Overall: 70 model requests, latency p50 1.646 s / p95 20.6285 s.
Recorder ↔ transcript cross-check: 28/29 transcript responses matched, 42 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-013835-s4_compaction_tester-incredible-four-rep4/`

### 20261029-013835-s4_compaction_tester-incredible-four-rep5 — s4_compaction_tester × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 4.5 | 1024.7 | 1028 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `40ec0895` Почините format_report (разделитель записей) (activated 2026-10-28T22:38:45.474523+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 3 | 3.644 | 1.486 | 1.4959 | 9197 | 399 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 53 | 977.672 | 1.698 | 43.5436 | 701956 | 26125 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 37.263 | 6.011 | 10.503 | 98423 | 10768 |

Overall: 61 model requests, latency p50 1.729 s / p95 20.396 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 51 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-013835-s4_compaction_tester-incredible-four-rep5/`

### 20261029-014015-s4_compaction_tester-incredible-four-rep6 — s4_compaction_tester × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 79.6 | 172.4 | 251.3 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `0a51c95d` Почините format_report (разделитель записей) (activated 2026-10-28T22:40:25.442427+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 25 | 80.426 | 1.378 | 10.664 | 978292 | 2139 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 32 | 135.041 | 1.521 | 16.0861 | 449779 | 6416 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 29.478 | 6.7925 | 9.0675 | 95070 | 6957 |

Overall: 61 model requests, latency p50 1.511 s / p95 14.368 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 30 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-014015-s4_compaction_tester-incredible-four-rep6/`

### 20261029-014441-s4_compaction_tester-incredible-four-rep7 — s4_compaction_tester × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 8.9 | 807.6 | 815.5 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `43bdff49` Почините format_report (разделитель записей) (activated 2026-10-28T22:44:48.647393+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 7.448 | 0.916 | 4.5457 | 12494 | 328 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 61 | 750.849 | 1.507 | 15.928 | 752057 | 29337 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 40.775 | 5.45 | 7.5191 | 134189 | 15826 |

Overall: 72 model requests, latency p50 1.758 s / p95 13.546 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 63 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-014441-s4_compaction_tester-incredible-four-rep7/`

### 20261029-014639-s4_compaction_tester-incredible-four-rep8 — s4_compaction_tester × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 10.3 | 635.3 | 644.7 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `0b31c1ce` Почините format_report (разделитель записей) (activated 2026-10-28T22:46:47.689932+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 10.962 | 1.7785 | 6.3188 | 12752 | 410 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 48 | 594.516 | 1.5635 | 11.6873 | 624149 | 17222 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 30.062 | 6.229 | 7.8038 | 105962 | 11027 |

Overall: 57 model requests, latency p50 1.668 s / p95 9.1616 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 47 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-014639-s4_compaction_tester-incredible-four-rep8/`

### 20261029-015558-s4_compaction_tester-incredible-four-rep9 — s4_compaction_tester × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 38.9 | 146.7 | 184.9 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `a9b494b9` Почините format_report (разделитель записей) (activated 2026-10-28T22:56:07.484943+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 27 | 35.261 | 1.065 | 2.3628 | 995408 | 1780 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 46 | 105.169 | 1.904 | 5.2678 | 510507 | 13843 |
| x5-airun-small-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 32.545 | 5.899 | 9.1364 | 104493 | 12575 |

Overall: 78 model requests, latency p50 1.6495 s / p95 6.0374 s.
Recorder ↔ transcript cross-check: 32/32 transcript responses matched, 46 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-015558-s4_compaction_tester-incredible-four-rep9/`

### 20261029-015736-s4_compaction_tester-regular-three-rep0 — s4_compaction_tester × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 30.6 | 71.4 | 101.4 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `c0c15477` Почините format_report (разделитель записей) (activated 2026-10-28T22:57:45.282264+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 25 | 29.041 | 0.96 | 2.0772 | 894811 | 1438 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 37 | 45.185 | 1.075 | 2.1586 | 508351 | 2300 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 5 | 15.983 | 3.114 | 3.8014 | 121869 | 4795 |

Overall: 67 model requests, latency p50 1.06 s / p95 3.0504 s.
Recorder ↔ transcript cross-check: 30/30 transcript responses matched, 37 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-015736-s4_compaction_tester-regular-three-rep0/`

### 20261029-015828-s4_compaction_tester-regular-three-rep1 — s4_compaction_tester × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 4 | 87.5 | 91 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `76086d08` Почините format_report (разделитель записей) (activated 2026-10-28T22:58:31.747464+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 3 | 2.932 | 0.872 | 1.4633 | 9515 | 450 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 59 | 62.872 | 0.975 | 2.0158 | 725036 | 3474 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 6 | 18.708 | 3.1475 | 3.6405 | 133688 | 5962 |

Overall: 68 model requests, latency p50 1.0165 s / p95 2.987 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 55 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-015828-s4_compaction_tester-regular-three-rep1/`

### 20261029-015917-s4_compaction_tester-regular-three-rep2 — s4_compaction_tester × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 29.6 | 160.8 | 189.7 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `50da1137` Почините format_report (разделитель записей) (activated 2026-10-28T22:59:25.327001+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 26 | 28.223 | 0.99 | 1.579 | 990877 | 2407 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 130 | 124.342 | 0.8675 | 1.7363 | 1820584 | 6996 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 8 | 22.885 | 2.8785 | 3.2518 | 175449 | 6722 |

Overall: 164 model requests, latency p50 0.9075 s / p95 2.3747 s.
Recorder ↔ transcript cross-check: 45/45 transcript responses matched, 119 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-015917-s4_compaction_tester-regular-three-rep2/`

### 20261029-015930-s4_compaction_tester-regular-three-rep3 — s4_compaction_tester × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 29.1 | 39 | 67.4 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `5e349066` Почините format_report (разделитель записей) (activated 2026-10-28T22:59:34.357941+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 24 | 28.01 | 1.065 | 2.0573 | 905508 | 2702 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 21 | 26.073 | 1.301 | 2.182 | 294188 | 1462 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 5.547 | 2.7735 | 2.7928 | 53099 | 1511 |

Overall: 47 model requests, latency p50 1.143 s / p95 2.5955 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 16 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-015930-s4_compaction_tester-regular-three-rep3/`

### 20261029-020006-s4_compaction_tester-regular-three-rep4 — s4_compaction_tester × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 33.6 | 51.8 | 84.4 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `6fc8b694` Почините format_report (разделитель записей) (activated 2026-10-28T23:00:10.098038+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 26 | 32.08 | 1.15 | 2.048 | 990174 | 2220 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 26 | 33.827 | 1.1505 | 2.5195 | 346000 | 2231 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 3 | 10.607 | 3.643 | 3.6484 | 70953 | 3484 |

Overall: 55 model requests, latency p50 1.179 s / p95 2.9587 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 24 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-020006-s4_compaction_tester-regular-three-rep4/`

### 20261029-020045-s4_compaction_tester-regular-three-rep5 — s4_compaction_tester × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 28.5 | 52.9 | 80.7 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `22c7fded` Почините format_report (разделитель записей) (activated 2026-10-28T23:00:54.172497+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 26 | 26.559 | 0.89 | 1.8855 | 972404 | 1321 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 30 | 38.581 | 1.1855 | 2.1816 | 419436 | 1840 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 4 | 10.785 | 2.6155 | 2.9886 | 98773 | 2836 |

Overall: 60 model requests, latency p50 1.067 s / p95 2.5292 s.
Recorder ↔ transcript cross-check: 30/30 transcript responses matched, 30 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-020045-s4_compaction_tester-regular-three-rep5/`

### 20261029-020140-s4_compaction_tester-regular-three-rep6 — s4_compaction_tester × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 31.9 | 77.4 | 108.8 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `7667758e` Почините format_report (разделитель записей) (activated 2026-10-28T23:01:45.064451+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 26 | 30.464 | 1.0955 | 2.298 | 990352 | 2048 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 40 | 52.055 | 1.146 | 2.1081 | 572567 | 2444 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 6 | 18.722 | 3.2575 | 3.3008 | 145874 | 6201 |

Overall: 72 model requests, latency p50 1.1585 s / p95 3.2574 s.
Recorder ↔ transcript cross-check: 29/29 transcript responses matched, 43 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-020140-s4_compaction_tester-regular-three-rep6/`

### 20261029-020219-s4_compaction_tester-regular-three-rep7 — s4_compaction_tester × regular-three

Reason: `settled but checks.py failed:
S4 checks FAILED:
- task 620e7e02: no data/listing.txt lines in the tester's run_bash tool-returns — the listing was never read (the brief's acceptance requirement)`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 33.6 | 27.4 | 60.6 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `620e7e02` Почините format_report (разделитель записей) (activated 2026-10-28T23:02:29.010014+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 26 | 31.521 | 0.915 | 1.9442 | 973021 | 1439 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 15 | 18.406 | 1.191 | 1.9601 | 210254 | 1132 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 2 | 6.056 | 3.028 | 3.4375 | 52955 | 1473 |

Overall: 43 model requests, latency p50 0.952 s / p95 2.5304 s.
Recorder ↔ transcript cross-check: 28/28 transcript responses matched, 15 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-020219-s4_compaction_tester-regular-three-rep7/`

### 20261029-020239-s4_compaction_tester-regular-three-rep8 — s4_compaction_tester × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 33.6 | 57.6 | 89.7 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `c3829486` Почините format_report (разделитель записей) (activated 2026-10-28T23:02:44.508802+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 27 | 31.774 | 0.976 | 2.5781 | 989921 | 1607 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 24 | 42.74 | 1.233 | 6.1658 | 323382 | 2223 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 3 | 11.508 | 4.1 | 4.5329 | 66069 | 3354 |

Overall: 54 model requests, latency p50 1.058 s / p95 4.8417 s.
Recorder ↔ transcript cross-check: 33/33 transcript responses matched, 21 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-020239-s4_compaction_tester-regular-three-rep8/`

### 20261029-020332-s4_compaction_tester-regular-three-rep9 — s4_compaction_tester × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините format_report (разделитель записей) | bug | completed | Verified successfully | 43.1 | 65.8 | 108.2 |

Tester compaction threshold source: tester model config — as expected (drcode ≥ 0.5.0: per-role config, §1.2).

Bug round-trips:

- `c0e143cd` Почините format_report (разделитель записей) (activated 2026-10-28T23:03:39.676786+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 24 | 39.897 | 1.27 | 5.206 | 899980 | 2124 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 35 | 45.668 | 1.132 | 2.4006 | 475745 | 2275 |
| x5-airun-small@https://api-copilot.x5.ru/aigw/v1 | 4 | 13.192 | 3.4145 | 3.5254 | 100031 | 3949 |

Overall: 63 model requests, latency p50 1.212 s / p95 3.5283 s.
Recorder ↔ transcript cross-check: 31/31 transcript responses matched, 32 unmatched recorder entries (compaction requests, §1.5) — UNEXPLAINED DISCREPANCIES.

Artifacts: `20261029-020332-s4_compaction_tester-regular-three-rep9/`

### 20261029-020535-s5_clarification-deepseek-v4-baseline-rep0 — s5_clarification × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 16 | 33.9 | 60.6 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 12 | 63.669 | 5.337 | 9.1327 | 45640 | 2731 |

Overall: 12 model requests, latency p50 5.337 s / p95 9.1327 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020535-s5_clarification-deepseek-v4-baseline-rep0/`

### 20261029-020550-s5_clarification-deepseek-v4-baseline-rep1 — s5_clarification × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 23.3 | 24.9 | 56.9 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 11 | 60.214 | 4.673 | 12.2205 | 41482 | 2818 |

Overall: 11 model requests, latency p50 4.673 s / p95 12.2205 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020550-s5_clarification-deepseek-v4-baseline-rep1/`

### 20261029-020551-s5_clarification-deepseek-v4-baseline-rep2 — s5_clarification × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 16.6 | 34 | 62.3 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 13 | 64.972 | 4.98 | 9.5442 | 74515 | 2969 |

Overall: 13 model requests, latency p50 4.98 s / p95 9.5442 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020551-s5_clarification-deepseek-v4-baseline-rep2/`

### 20261029-020645-s5_clarification-deepseek-v4-baseline-rep3 — s5_clarification × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 26.1 | 35.6 | 72.6 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 15 | 71.828 | 5.198 | 7.8377 | 56448 | 3539 |

Overall: 15 model requests, latency p50 5.198 s / p95 7.8377 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020645-s5_clarification-deepseek-v4-baseline-rep3/`

### 20261029-020702-s5_clarification-deepseek-v4-baseline-rep4 — s5_clarification × deepseek-v4-baseline

Reason: `scenario failure: task 'Реализуйте format_price()' (7a6cbec6) awaits clarification but no scenario answer matches: "Repo contains no spec for the price format (prices.py is just a stub, no tests/examples/docs). What is the corporate standard for formatting prices that format_price(amount, currency='RUB') must follow? Please describe it precisely — e.g. how many decimal places, the decimal/thousands separators (dot/comma/space), currency symbol or code, placement before/after the number, currency-specific differences, negative amounts, and any rounding behavior."`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | clarification | — | 11.7 | — | — |

User-simulator interventions: 0 (failure: 1, start: 1)
- SIM FAILURE: task 'Реализуйте format_price()' (7a6cbec6) awaits clarification but no scenario answer matches: "Repo contains no spec for the price format (prices.py is just a stub, no tests/examples/docs). What is the corporate standard for formatting prices that format_price(amount, currency='RUB') must follow? Please describe it precisely — e.g. how many decimal places, the decimal/thousands separators (dot/comma/space), currency symbol or code, placement before/after the number, currency-specific differences, negative amounts, and any rounding behavior."

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 12.405 | 1.8535 | 6.6519 | 11887 | 579 |

Overall: 4 model requests, latency p50 1.8535 s / p95 6.6519 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020702-s5_clarification-deepseek-v4-baseline-rep4/`

### 20261029-020708-s5_clarification-deepseek-v4-baseline-rep5 — s5_clarification × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 25.5 | 23.5 | 67.2 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 15 | 67.928 | 3.667 | 10.4852 | 90051 | 3180 |

Overall: 15 model requests, latency p50 3.667 s / p95 10.4852 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020708-s5_clarification-deepseek-v4-baseline-rep5/`

### 20261029-020725-s5_clarification-deepseek-v4-baseline-rep6 — s5_clarification × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 19.2 | 26.7 | 58.4 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 12 | 60.446 | 3.8645 | 11.4377 | 42520 | 3056 |

Overall: 12 model requests, latency p50 3.8645 s / p95 11.4377 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020725-s5_clarification-deepseek-v4-baseline-rep6/`

### 20261029-020804-s5_clarification-deepseek-v4-baseline-rep7 — s5_clarification × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 17.1 | 32.9 | 58.3 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 13 | 60.84 | 4.327 | 8.2556 | 65584 | 2968 |

Overall: 13 model requests, latency p50 4.327 s / p95 8.2556 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020804-s5_clarification-deepseek-v4-baseline-rep7/`

### 20261029-020822-s5_clarification-deepseek-v4-baseline-rep8 — s5_clarification × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 13.2 | 25.5 | 48.9 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 11 | 50.611 | 2.944 | 8.8695 | 43158 | 2475 |

Overall: 11 model requests, latency p50 2.944 s / p95 8.8695 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020822-s5_clarification-deepseek-v4-baseline-rep8/`

### 20261029-020833-s5_clarification-deepseek-v4-baseline-rep9 — s5_clarification × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 17.1 | 30.7 | 55.7 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 13 | 58.557 | 4.088 | 9.8796 | 51608 | 2905 |

Overall: 13 model requests, latency p50 4.088 s / p95 9.8796 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020833-s5_clarification-deepseek-v4-baseline-rep9/`

### 20261029-020337-s5_clarification-glm-5.3-baseline-rep0 — s5_clarification × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 7 | 14.9 | 25.5 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 25.345 | 1.537 | 3.6512 | 57966 | 3027 |

Overall: 15 model requests, latency p50 1.537 s / p95 3.6512 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020337-s5_clarification-glm-5.3-baseline-rep0/`

### 20261029-020410-s5_clarification-glm-5.3-baseline-rep1 — s5_clarification × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.3 | 5.3 | 11.5 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 11 | 12.239 | 1.005 | 1.901 | 35888 | 1499 |

Overall: 11 model requests, latency p50 1.005 s / p95 1.901 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020410-s5_clarification-glm-5.3-baseline-rep1/`

### 20261029-020419-s5_clarification-glm-5.3-baseline-rep2 — s5_clarification × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 3.5 | 4 | 10.5 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 11 | 9.876 | 0.684 | 1.668 | 37355 | 1343 |

Overall: 11 model requests, latency p50 0.684 s / p95 1.668 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020419-s5_clarification-glm-5.3-baseline-rep2/`

### 20261029-020427-s5_clarification-glm-5.3-baseline-rep3 — s5_clarification × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 3.8 | 5.6 | 12.2 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 11 | 12.941 | 1.064 | 2.03 | 39567 | 1930 |

Overall: 11 model requests, latency p50 1.064 s / p95 2.03 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020427-s5_clarification-glm-5.3-baseline-rep3/`

### 20261029-020436-s5_clarification-glm-5.3-baseline-rep4 — s5_clarification × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.9 | 8.7 | 18 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 16.899 | 0.826 | 2.7888 | 49359 | 2494 |

Overall: 13 model requests, latency p50 0.826 s / p95 2.7888 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020436-s5_clarification-glm-5.3-baseline-rep4/`

### 20261029-020446-s5_clarification-glm-5.3-baseline-rep5 — s5_clarification × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 5.1 | 12.2 | 19.7 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 21.014 | 1.188 | 4.7356 | 40896 | 1962 |

Overall: 12 model requests, latency p50 1.188 s / p95 4.7356 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020446-s5_clarification-glm-5.3-baseline-rep5/`

### 20261029-020505-s5_clarification-glm-5.3-baseline-rep6 — s5_clarification × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.5 | 10.2 | 19.8 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 18.42 | 1.228 | 2.8698 | 48550 | 2455 |

Overall: 13 model requests, latency p50 1.228 s / p95 2.8698 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020505-s5_clarification-glm-5.3-baseline-rep6/`

### 20261029-020515-s5_clarification-glm-5.3-baseline-rep7 — s5_clarification × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 6.1 | 5.4 | 14.3 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 14.543 | 0.983 | 2.7091 | 41396 | 2299 |

Overall: 12 model requests, latency p50 0.983 s / p95 2.7091 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020515-s5_clarification-glm-5.3-baseline-rep7/`

### 20261029-020531-s5_clarification-glm-5.3-baseline-rep8 — s5_clarification × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 3.6 | 5.5 | 12.1 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 12.607 | 0.845 | 1.9982 | 42014 | 2154 |

Overall: 12 model requests, latency p50 0.845 s / p95 1.9982 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020531-s5_clarification-glm-5.3-baseline-rep8/`

### 20261029-020531-s5_clarification-glm-5.3-baseline-rep9 — s5_clarification × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 3.2 | 7.7 | 13.8 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 12.713 | 0.793 | 1.717 | 46771 | 2077 |

Overall: 13 model requests, latency p50 0.793 s / p95 1.717 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020531-s5_clarification-glm-5.3-baseline-rep9/`

### 20261029-020919-s5_clarification-incredible-four-rep0 — s5_clarification × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.2 | 15.4 | 23.5 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 7.865 | 0.756 | 2.4956 | 23275 | 1433 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 13.381 | 1.57 | 3.5126 | 29872 | 2331 |

Overall: 14 model requests, latency p50 1.2045 s / p95 3.3768 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020919-s5_clarification-incredible-four-rep0/`

### 20261029-020920-s5_clarification-incredible-four-rep1 — s5_clarification × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.5 | 17.8 | 24.5 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 7.474 | 0.93 | 1.5151 | 22589 | 1082 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 17.862 | 2.291 | 5.0001 | 41536 | 3317 |

Overall: 14 model requests, latency p50 1.389 s / p95 4.46 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020920-s5_clarification-incredible-four-rep1/`

### 20261029-020938-s5_clarification-incredible-four-rep2 — s5_clarification × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.3 | 22.2 | 29.1 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 7.145 | 0.9 | 1.7565 | 23365 | 1153 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 19.522 | 1.665 | 5.1845 | 40247 | 3084 |

Overall: 15 model requests, latency p50 1.233 s / p95 4.46 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020938-s5_clarification-incredible-four-rep2/`

### 20261029-020956-s5_clarification-incredible-four-rep3 — s5_clarification × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 6.6 | 25.4 | 34.8 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 9.522 | 1.161 | 3.8972 | 18966 | 828 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 22.55 | 3.098 | 6.2506 | 73095 | 3962 |

Overall: 13 model requests, latency p50 1.285 s / p95 5.8312 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020956-s5_clarification-incredible-four-rep3/`

### 20261029-020958-s5_clarification-incredible-four-rep4 — s5_clarification × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 9.6 | 24.8 | 37.6 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 13.554 | 0.847 | 6.2762 | 23150 | 1506 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 23.761 | 3.425 | 6.4544 | 39938 | 4448 |

Overall: 14 model requests, latency p50 1.364 s / p95 7.1483 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-020958-s5_clarification-incredible-four-rep4/`

### 20261029-021014-s5_clarification-incredible-four-rep5 — s5_clarification × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.3 | 22.9 | 29.1 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 7.164 | 0.943 | 2.0667 | 21983 | 960 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 20.234 | 2.713 | 5.6357 | 68449 | 3423 |

Overall: 14 model requests, latency p50 1.048 s / p95 4.9108 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021014-s5_clarification-incredible-four-rep5/`

### 20261029-021038-s5_clarification-incredible-four-rep6 — s5_clarification × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 5.2 | 42.3 | 50.7 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 9.807 | 0.793 | 3.2234 | 23011 | 1584 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 11 | 39.233 | 3.079 | 6.47 | 128084 | 6631 |

Overall: 18 model requests, latency p50 2.2685 s / p95 5.616 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021038-s5_clarification-incredible-four-rep6/`

### 20261029-021043-s5_clarification-incredible-four-rep7 — s5_clarification × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.7 | 22.9 | 29.3 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 8.245 | 0.968 | 1.7828 | 22366 | 1197 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 19.255 | 1.415 | 4.3558 | 59793 | 3227 |

Overall: 16 model requests, latency p50 1.3475 s / p95 3.6618 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021043-s5_clarification-incredible-four-rep7/`

### 20261029-021050-s5_clarification-incredible-four-rep8 — s5_clarification × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.1 | 26.5 | 32.6 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 6.817 | 0.921 | 2.2822 | 18934 | 964 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 24.616 | 4.124 | 6.5099 | 39639 | 4277 |

Overall: 13 model requests, latency p50 1.383 s / p95 5.9858 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021050-s5_clarification-incredible-four-rep8/`

### 20261029-021120-s5_clarification-incredible-four-rep9 — s5_clarification × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.6 | 29.9 | 37.1 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 8.019 | 0.71 | 2.6888 | 22617 | 1481 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 27.155 | 2.19 | 7.2518 | 106189 | 4325 |

Overall: 16 model requests, latency p50 1.4045 s / p95 5.7422 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021120-s5_clarification-incredible-four-rep9/`

### 20261029-021129-s5_clarification-regular-three-rep0 — s5_clarification × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.3 | 5.9 | 14.7 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 9.002 | 0.968 | 2.1033 | 28090 | 1714 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 5.153 | 0.869 | 1.143 | 21822 | 596 |

Overall: 14 model requests, latency p50 0.889 s / p95 1.9896 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021129-s5_clarification-regular-three-rep0/`

### 20261029-021141-s5_clarification-regular-three-rep1 — s5_clarification × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4 | 7.4 | 13.6 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 6.166 | 0.782 | 1.3059 | 21796 | 946 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 6.732 | 0.667 | 1.2308 | 31849 | 980 |

Overall: 15 model requests, latency p50 0.763 s / p95 1.2861 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021141-s5_clarification-regular-three-rep1/`

### 20261029-021151-s5_clarification-regular-three-rep2 — s5_clarification × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4 | 8.6 | 14.7 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 6.494 | 1.0045 | 1.663 | 18686 | 884 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 6.187 | 1.0025 | 1.5378 | 22468 | 928 |

Overall: 12 model requests, latency p50 1.0025 s / p95 1.7041 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021151-s5_clarification-regular-three-rep2/`

### 20261029-021204-s5_clarification-regular-three-rep3 — s5_clarification × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 2.1 | 8.1 | 35.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Реализуйте format_price()', 'tester': 'feature:Реализуйте format_price() round 0', 'at': '2026-10-28T23:12:33.071431+00:00', 'detail': 'coder message at 2026-10-28T23:12:33.071431+00:00 inside tester interval 2026-10-28T23:12:20.499901+00:00…2026-10-28T23:12:33.544324+00:00'}

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 12.545 | 0.865 | 2.9972 | 39460 | 2034 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 14 | 20.339 | 1.235 | 2.9504 | 64157 | 2372 |

Overall: 24 model requests, latency p50 1.1385 s / p95 3.7969 s.
Recorder ↔ transcript cross-check: 24/24 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021204-s5_clarification-regular-three-rep3/`

### 20261029-021205-s5_clarification-regular-three-rep4 — s5_clarification × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.1 | 11.4 | 18.6 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 7.899 | 0.987 | 2.0669 | 22619 | 1220 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 7 | 10.579 | 1.08 | 3.8562 | 29817 | 999 |

Overall: 14 model requests, latency p50 1.006 s / p95 3.1562 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021205-s5_clarification-regular-three-rep4/`

### 20261029-021212-s5_clarification-regular-three-rep5 — s5_clarification × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 8.5 | 6.7 | 18.2 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 12.066 | 1.0365 | 5.5778 | 20839 | 1722 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 5.728 | 1.0005 | 1.3942 | 25411 | 917 |

Overall: 12 model requests, latency p50 1.0365 s / p95 3.985 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021212-s5_clarification-regular-three-rep5/`

### 20261029-021230-s5_clarification-regular-three-rep6 — s5_clarification × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 6.8 | 10.4 | 19.4 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 9.179 | 0.989 | 1.9783 | 27888 | 1584 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 7 | 7.558 | 0.809 | 1.6666 | 30343 | 1288 |

Overall: 15 model requests, latency p50 0.906 s / p95 1.8439 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021230-s5_clarification-regular-three-rep6/`

### 20261029-021236-s5_clarification-regular-three-rep7 — s5_clarification × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.4 | 11.3 | 17.7 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 6.547 | 0.9735 | 1.967 | 19081 | 1173 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 7 | 9.399 | 1.255 | 2.128 | 59077 | 1246 |

Overall: 13 model requests, latency p50 1.049 s / p95 2.225 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021236-s5_clarification-regular-three-rep7/`

### 20261029-021246-s5_clarification-regular-three-rep8 — s5_clarification × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 5.2 | 7.3 | 14.8 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 7.82 | 0.795 | 3.2512 | 20603 | 1746 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 7.102 | 1.1445 | 1.8162 | 22784 | 1210 |

Overall: 12 model requests, latency p50 0.8125 s / p95 2.8303 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021246-s5_clarification-regular-three-rep8/`

### 20261029-021258-s5_clarification-regular-three-rep9 — s5_clarification × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте format_price() | feature | completed | Verified successfully | 4.9 | 11.3 | 19.1 |

User-simulator interventions: 1 (clarification_answer: 1, start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 8.553 | 1.2275 | 2.6445 | 20394 | 1491 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 9 | 8.146 | 0.682 | 1.6148 | 37987 | 1199 |

Overall: 15 model requests, latency p50 1.121 s / p95 2.1388 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021258-s5_clarification-regular-three-rep9/`

### 20261029-021507-s6_queue_priority-deepseek-v4-baseline-rep0 — s6_queue_priority × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 20.5 | 22.9 | 94.1 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 9 | 38.2 | 46.6 |

Bug round-trips:

- `aa2d4f0e` Почините median() для чётной длины (activated 2026-10-28T23:15:16.289069+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 22 | 83.279 | 3.1145 | 6.5046 | 86190 | 4249 |

Overall: 22 model requests, latency p50 3.1145 s / p95 6.5046 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021507-s6_queue_priority-deepseek-v4-baseline-rep0/`

### 20261029-021514-s6_queue_priority-deepseek-v4-baseline-rep1 — s6_queue_priority × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 12.8 | 18 | 64.2 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 11.8 | 20 | 31.3 |

Bug round-trips:

- `dbccabca` Почините median() для чётной длины (activated 2026-10-28T23:15:18.591840+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 19 | 57.746 | 2.712 | 5.6117 | 65497 | 2802 |

Overall: 19 model requests, latency p50 2.712 s / p95 5.6117 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021514-s6_queue_priority-deepseek-v4-baseline-rep1/`

### 20261029-021520-s6_queue_priority-deepseek-v4-baseline-rep2 — s6_queue_priority × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 9.6 | 47.8 | 56 |
| Реализуйте stdev() | feature | completed | Verified successfully | 13.4 | 24.9 | 100 |

Bug round-trips:

- `6dac819d` Почините median() для чётной длины (activated 2026-10-28T23:15:24.399681+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 24 | 91.513 | 3.1045 | 9.4106 | 110059 | 4648 |

Overall: 24 model requests, latency p50 3.1045 s / p95 9.4106 s.
Recorder ↔ transcript cross-check: 24/24 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021520-s6_queue_priority-deepseek-v4-baseline-rep2/`

### 20261029-021628-s6_queue_priority-deepseek-v4-baseline-rep3 — s6_queue_priority × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 9.8 | 21 | 84.2 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 10.6 | 37.9 | 47.7 |

Bug round-trips:

- `35ff437c` Почините median() для чётной длины (activated 2026-10-28T23:16:36.342142+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 21 | 76.581 | 2.624 | 9.343 | 74332 | 3911 |

Overall: 21 model requests, latency p50 2.624 s / p95 9.343 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021628-s6_queue_priority-deepseek-v4-baseline-rep3/`

### 20261029-021653-s6_queue_priority-deepseek-v4-baseline-rep4 — s6_queue_priority × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 10.4 | 18.2 | 28 |
| Реализуйте stdev() | feature | completed | Verified successfully | 10.1 | 17.9 | 59.2 |

Bug round-trips:

- `1dfc9860` Почините median() для чётной длины (activated 2026-10-28T23:16:57.623573+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 19 | 53.873 | 2.529 | 4.0441 | 64920 | 2473 |

Overall: 19 model requests, latency p50 2.529 s / p95 4.0441 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021653-s6_queue_priority-deepseek-v4-baseline-rep4/`

### 20261029-021710-s6_queue_priority-deepseek-v4-baseline-rep5 — s6_queue_priority × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 10.3 | 21.7 | 31.5 |
| Реализуйте stdev() | feature | completed | Verified successfully | 11 | 26.7 | 72.2 |

Bug round-trips:

- `93fdd3ac` Почините median() для чётной длины (activated 2026-10-28T23:17:14.279353+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 22 | 64.714 | 2.58 | 5.091 | 80466 | 3166 |

Overall: 22 model requests, latency p50 2.58 s / p95 5.091 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021710-s6_queue_priority-deepseek-v4-baseline-rep5/`

### 20261029-021802-s6_queue_priority-deepseek-v4-baseline-rep6 — s6_queue_priority × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 9 | 38.1 | 46.5 |
| Реализуйте stdev() | feature | completed | Verified successfully | 9.5 | 16 | 77.8 |

Bug round-trips:

- `04511670` Почините median() для чётной длины (activated 2026-10-28T23:18:10.471761+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 23 | 68.887 | 2.83 | 6.2449 | 88135 | 3608 |

Overall: 23 model requests, latency p50 2.83 s / p95 6.2449 s.
Recorder ↔ transcript cross-check: 23/23 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021802-s6_queue_priority-deepseek-v4-baseline-rep6/`

### 20261029-021806-s6_queue_priority-deepseek-v4-baseline-rep7 — s6_queue_priority × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 11.6 | 21.8 | 61.8 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 10.1 | 18.1 | 27.7 |

Bug round-trips:

- `96e1a373` Почините median() для чётной длины (activated 2026-10-28T23:18:10.549036+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 22 | 56.339 | 2.277 | 4.3899 | 77509 | 2696 |

Overall: 22 model requests, latency p50 2.277 s / p95 4.3899 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021806-s6_queue_priority-deepseek-v4-baseline-rep7/`

### 20261029-021831-s6_queue_priority-deepseek-v4-baseline-rep8 — s6_queue_priority × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 10.9 | 11.8 | 22.2 |
| Реализуйте stdev() | feature | completed | Verified successfully | 15.5 | 19 | 58.8 |

Bug round-trips:

- `923a94dd` Почините median() для чётной длины (activated 2026-10-28T23:18:35.470851+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 19 | 53.492 | 2.459 | 4.5189 | 64853 | 2506 |

Overall: 19 model requests, latency p50 2.459 s / p95 4.5189 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021831-s6_queue_priority-deepseek-v4-baseline-rep8/`

### 20261029-021918-s6_queue_priority-deepseek-v4-baseline-rep9 — s6_queue_priority × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 8.5 | 29.5 | 37.5 |
| Реализуйте stdev() | feature | completed | Verified successfully | 23.7 | 22.6 | 86.8 |

Bug round-trips:

- `884314d2` Почините median() для чётной длины (activated 2026-10-28T23:19:26.472070+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 23 | 73.078 | 2.502 | 5.8588 | 87628 | 3935 |

Overall: 23 model requests, latency p50 2.502 s / p95 5.8588 s.
Recorder ↔ transcript cross-check: 23/23 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021918-s6_queue_priority-deepseek-v4-baseline-rep9/`

### 20261029-021300-s6_queue_priority-glm-5.3-baseline-rep0 — s6_queue_priority × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 4 | 8.3 | 11.8 |
| Реализуйте stdev() | feature | completed | Verified successfully | 3.7 | 7.4 | 23.6 |

Bug round-trips:

- `df7f3e64` Почините median() для чётной длины (activated 2026-10-28T23:13:04.452824+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 19 | 13.766 | 0.642 | 1.1389 | 63201 | 1748 |

Overall: 19 model requests, latency p50 0.642 s / p95 1.1389 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021300-s6_queue_priority-glm-5.3-baseline-rep0/`

### 20261029-021311-s6_queue_priority-glm-5.3-baseline-rep1 — s6_queue_priority × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 5.7 | 5.8 | 11.2 |
| Реализуйте stdev() | feature | completed | Verified successfully | 7.3 | 12.2 | 31.1 |

Bug round-trips:

- `44546432` Почините median() для чётной длины (activated 2026-10-28T23:13:16.195749+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 25 | 18.794 | 0.66 | 1.0518 | 85131 | 1595 |

Overall: 25 model requests, latency p50 0.66 s / p95 1.0518 s.
Recorder ↔ transcript cross-check: 25/25 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021311-s6_queue_priority-glm-5.3-baseline-rep1/`

### 20261029-021323-s6_queue_priority-glm-5.3-baseline-rep2 — s6_queue_priority × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 3.5 | 10.7 | 13.9 |
| Реализуйте stdev() | feature | completed | Verified successfully | 7.8 | 10.4 | 32.5 |

Bug round-trips:

- `7e032b06` Почините median() для чётной длины (activated 2026-10-28T23:13:27.968535+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 22 | 18.588 | 0.6915 | 1.5309 | 76678 | 2083 |

Overall: 22 model requests, latency p50 0.6915 s / p95 1.5309 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021323-s6_queue_priority-glm-5.3-baseline-rep2/`

### 20261029-021331-s6_queue_priority-glm-5.3-baseline-rep3 — s6_queue_priority × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 4.9 | 11.9 | 28.4 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.8 | 7 | 11.2 |

Bug round-trips:

- `e524f787` Почините median() для чётной длины (activated 2026-10-28T23:13:36.155952+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 25 | 18.418 | 0.61 | 1.6402 | 85970 | 1934 |

Overall: 25 model requests, latency p50 0.61 s / p95 1.6402 s.
Recorder ↔ transcript cross-check: 25/25 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021331-s6_queue_priority-glm-5.3-baseline-rep3/`

### 20261029-021351-s6_queue_priority-glm-5.3-baseline-rep4 — s6_queue_priority × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.4 | 7.7 | 11.3 |
| Реализуйте stdev() | feature | completed | Verified successfully | 4.5 | 11 | 27.8 |

Bug round-trips:

- `43a5b652` Почините median() для чётной длины (activated 2026-10-28T23:14:00.587892+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 20 | 16.926 | 0.6825 | 1.6241 | 69684 | 1570 |

Overall: 20 model requests, latency p50 0.6825 s / p95 1.6241 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021351-s6_queue_priority-glm-5.3-baseline-rep4/`

### 20261029-021404-s6_queue_priority-glm-5.3-baseline-rep5 — s6_queue_priority × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 4.6 | 8.5 | 24.1 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.5 | 6.5 | 10.5 |

Bug round-trips:

- `d252fedc` Почините median() для чётной длины (activated 2026-10-28T23:14:08.244407+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 21 | 15.215 | 0.602 | 1.31 | 69045 | 1674 |

Overall: 21 model requests, latency p50 0.602 s / p95 1.31 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021404-s6_queue_priority-glm-5.3-baseline-rep5/`

### 20261029-021407-s6_queue_priority-glm-5.3-baseline-rep6 — s6_queue_priority × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 6.2 | 9.5 | 29.8 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 5 | 8.6 | 13.1 |

Bug round-trips:

- `48b4822b` Почините median() для чётной длины (activated 2026-10-28T23:14:11.420365+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 20 | 15.733 | 0.6995 | 1.4641 | 68598 | 1588 |

Overall: 20 model requests, latency p50 0.6995 s / p95 1.4641 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021407-s6_queue_priority-glm-5.3-baseline-rep6/`

### 20261029-021432-s6_queue_priority-glm-5.3-baseline-rep7 — s6_queue_priority × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.8 | 6.9 | 11 |
| Реализуйте stdev() | feature | completed | Verified successfully | 4.7 | 8.6 | 25.4 |

Bug round-trips:

- `8b0a9be6` Почините median() для чётной длины (activated 2026-10-28T23:14:38.487671+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 22 | 16.91 | 0.685 | 1.2105 | 75026 | 1678 |

Overall: 22 model requests, latency p50 0.685 s / p95 1.2105 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021432-s6_queue_priority-glm-5.3-baseline-rep7/`

### 20261029-021437-s6_queue_priority-glm-5.3-baseline-rep8 — s6_queue_priority × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 6.3 | 11.4 | 28.4 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 3.9 | 6.7 | 10 |

Bug round-trips:

- `a8959ed6` Почините median() для чётной длины (activated 2026-10-28T23:14:41.851673+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 24 | 16.766 | 0.6225 | 1.2629 | 87274 | 1560 |

Overall: 24 model requests, latency p50 0.6225 s / p95 1.2629 s.
Recorder ↔ transcript cross-check: 24/24 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021437-s6_queue_priority-glm-5.3-baseline-rep8/`

### 20261029-021444-s6_queue_priority-glm-5.3-baseline-rep9 — s6_queue_priority × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.6 | 6.6 | 10.8 |
| Реализуйте stdev() | feature | completed | Verified successfully | 9.5 | 8.5 | 29.5 |

Bug round-trips:

- `a3799665` Почините median() для чётной длины (activated 2026-10-28T23:14:48.384693+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 21 | 16.642 | 0.708 | 1.077 | 76262 | 1663 |

Overall: 21 model requests, latency p50 0.708 s / p95 1.077 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021444-s6_queue_priority-glm-5.3-baseline-rep9/`

### 20261029-021932-s6_queue_priority-incredible-four-rep0 — s6_queue_priority × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 6.6 | 16.5 | 40.6 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 3.8 | 13.2 | 16.5 |

Bug round-trips:

- `8b08a87d` Почините median() для чётной длины (activated 2026-10-28T23:19:35.848081+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 6.084 | 0.629 | 0.9888 | 26261 | 620 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 14 | 24.699 | 1.2875 | 3.7692 | 66711 | 3364 |

Overall: 23 model requests, latency p50 0.865 s / p95 2.694 s.
Recorder ↔ transcript cross-check: 23/23 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021932-s6_queue_priority-incredible-four-rep0/`

### 20261029-021940-s6_queue_priority-incredible-four-rep1 — s6_queue_priority × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 6.5 | 10.8 | 51.7 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.6 | 29.2 | 32.9 |

Bug round-trips:

- `768b3edc` Почините median() для чётной длины (activated 2026-10-28T23:19:44.131920+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 6.921 | 0.5175 | 0.8167 | 34241 | 644 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 15 | 35.61 | 1.908 | 5.9043 | 86483 | 5929 |

Overall: 27 model requests, latency p50 1.049 s / p95 4.9758 s.
Recorder ↔ transcript cross-check: 27/27 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-021940-s6_queue_priority-incredible-four-rep1/`

### 20261029-022021-s6_queue_priority-incredible-four-rep2 — s6_queue_priority × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 4.1 | 20.5 | 101.6 |
| test_stdev.py fails to collect: stdev() does not exist in stats.py (pre-existing, seed state) | bug | completed | Verified successfully | 5.2 | 38.8 | 45.9 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.4 | 25.8 | 26.4 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:test_stdev.py fails to collect: stdev() does not exist in stats.py (pre-existing, seed state)', 'tester': 'bug:Почините median() для чётной длины round 0', 'at': '2026-10-28T23:20:58.723425+00:00', 'detail': 'coder message at 2026-10-28T23:20:58.723425+00:00 inside tester interval 2026-10-28T23:20:33.737337+00:00…2026-10-28T23:20:59.270102+00:00'}

Bug round-trips:

- `6a0a516a` test_stdev.py fails to collect: stdev() does not exist in stats.py (pre-existing, seed state) (activated 2026-10-28T23:21:01.294122+00:00)
- `7199450c` Почините median() для чётной длины (activated 2026-10-28T23:20:29.081284+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 10.749 | 0.678 | 1.7282 | 33609 | 1408 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 25 | 76.009 | 2.003 | 9.098 | 201294 | 11581 |

Overall: 37 model requests, latency p50 1.376 s / p95 8.492 s.
Recorder ↔ transcript cross-check: 37/37 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022021-s6_queue_priority-incredible-four-rep2/`

### 20261029-022040-s6_queue_priority-incredible-four-rep3 — s6_queue_priority × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 3.7 | 30 | 29.5 |
| Реализуйте stdev() | feature | completed | Verified successfully | 9.9 | 9.6 | 95.7 |
| test_stdev.py red: `stdev` not yet in stats.py (owned by separate queued task) | bug | completed | Verified successfully | 8 | 32.8 | 41.7 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:test_stdev.py red: `stdev` not yet in stats.py (owned by separate queued task)', 'tester': 'bug:Почините median() для чётной длины round 0', 'at': '2026-10-28T23:21:17.745633+00:00', 'detail': 'coder message at 2026-10-28T23:21:17.745633+00:00 inside tester interval 2026-10-28T23:20:48.851665+00:00…2026-10-28T23:21:18.566779+00:00'}

Bug round-trips:

- `0035f30c` Почините median() для чётной длины (activated 2026-10-28T23:20:44.844189+00:00)
- `f2afc2ac` test_stdev.py red: `stdev` not yet in stats.py (owned by separate queued task) (activated 2026-10-28T23:21:19.641608+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 15.925 | 0.7635 | 3.4977 | 36005 | 1862 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 22 | 60.884 | 2.254 | 6.8094 | 137998 | 10341 |

Overall: 34 model requests, latency p50 1.8995 s / p95 6.3828 s.
Recorder ↔ transcript cross-check: 34/34 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022040-s6_queue_priority-incredible-four-rep3/`

### 20261029-022058-s6_queue_priority-incredible-four-rep4 — s6_queue_priority × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 4.9 | 14.8 | 85.3 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.1 | 28 | 29 |
| Full test suite fails to collect: test_stdev.py imports undefined stdev() | bug | completed | Verified successfully | 5 | 27.3 | 32.6 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:Full test suite fails to collect: test_stdev.py imports undefined stdev()', 'tester': 'bug:Почините median() для чётной длины round 0', 'at': '2026-10-28T23:21:33.677720+00:00', 'detail': 'coder message at 2026-10-28T23:21:33.677720+00:00 inside tester interval 2026-10-28T23:21:06.739611+00:00…2026-10-28T23:21:34.345362+00:00'}

Bug round-trips:

- `78351ef3` Почините median() для чётной длины (activated 2026-10-28T23:21:02.256070+00:00)
- `9461ca6b` Full test suite fails to collect: test_stdev.py imports undefined stdev() (activated 2026-10-28T23:21:35.280854+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 10.025 | 0.617 | 1.3128 | 40489 | 1370 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 21 | 59.791 | 2.036 | 7.314 | 153957 | 8902 |

Overall: 35 model requests, latency p50 1.087 s / p95 6.4838 s.
Recorder ↔ transcript cross-check: 35/35 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022058-s6_queue_priority-incredible-four-rep4/`

### 20261029-022214-s6_queue_priority-incredible-four-rep5 — s6_queue_priority × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 5.1 | 10.6 | 49.7 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 6.2 | 26.9 | 32.6 |

Bug round-trips:

- `dc522ddd` Почините median() для чётной длины (activated 2026-10-28T23:22:22.770139+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 6.86 | 0.684 | 1.2252 | 25356 | 688 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 14 | 30.808 | 2.0035 | 4.3446 | 75691 | 5079 |

Overall: 23 model requests, latency p50 1.038 s / p95 3.1795 s.
Recorder ↔ transcript cross-check: 23/23 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022214-s6_queue_priority-incredible-four-rep5/`

### 20261029-022224-s6_queue_priority-incredible-four-rep6 — s6_queue_priority × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.8 | 18 | 22.1 |
| Реализуйте stdev() | feature | completed | Verified successfully | 7.4 | 17.5 | 48.1 |

Bug round-trips:

- `4042e06e` Почините median() для чётной длины (activated 2026-10-28T23:22:29.713388+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 8.158 | 0.6615 | 0.9621 | 35907 | 749 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 14 | 30.707 | 1.7715 | 3.9383 | 110915 | 4634 |

Overall: 26 model requests, latency p50 0.848 s / p95 3.6455 s.
Recorder ↔ transcript cross-check: 26/26 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022224-s6_queue_priority-incredible-four-rep6/`

### 20261029-022231-s6_queue_priority-incredible-four-rep7 — s6_queue_priority × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 5.5 | 20.5 | 66.6 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 3.9 | 36.2 | 39.1 |

Bug round-trips:

- `da811771` Почините median() для чётной длины (activated 2026-10-28T23:22:36.208874+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 5.806 | 0.622 | 0.8748 | 25878 | 667 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 50.878 | 2.4085 | 7.8782 | 149555 | 8125 |

Overall: 25 model requests, latency p50 0.985 s / p95 6.3658 s.
Recorder ↔ transcript cross-check: 25/25 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022231-s6_queue_priority-incredible-four-rep7/`

### 20261029-022316-s6_queue_priority-incredible-four-rep8 — s6_queue_priority × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 3.9 | 35.5 | 37.8 |
| Реализуйте stdev() | feature | completed | Verified successfully | 7.6 | 11.7 | 59.4 |

Bug round-trips:

- `317e5eb6` Почините median() для чётной длины (activated 2026-10-28T23:23:23.875278+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 6.265 | 0.6295 | 0.8635 | 31642 | 620 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 13 | 42.957 | 2.369 | 9.4154 | 90996 | 7017 |

Overall: 23 model requests, latency p50 0.963 s / p95 5.8868 s.
Recorder ↔ transcript cross-check: 23/23 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022316-s6_queue_priority-incredible-four-rep8/`

### 20261029-022322-s6_queue_priority-incredible-four-rep9 — s6_queue_priority × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.6 | 26.8 | 30.5 |
| Реализуйте stdev() | feature | completed | Verified successfully | 4.2 | 12.9 | 48.7 |

Bug round-trips:

- `9b18c999` Почините median() для чётной длины (activated 2026-10-28T23:23:26.284662+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 5.663 | 0.657 | 0.8822 | 25649 | 540 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 15 | 33.568 | 1.543 | 5.3335 | 132040 | 4886 |

Overall: 24 model requests, latency p50 0.974 s / p95 4.606 s.
Recorder ↔ transcript cross-check: 24/24 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022322-s6_queue_priority-incredible-four-rep9/`

### 20261029-022347-s6_queue_priority-regular-three-rep0 — s6_queue_priority × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.5 | 6.1 | 10.2 |
| Реализуйте stdev() | feature | completed | Verified successfully | 6 | 8.8 | 25.2 |

Bug round-trips:

- `b15a902f` Почините median() для чётной длины (activated 2026-10-28T23:23:51.074758+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 11 | 6.824 | 0.572 | 0.9665 | 30757 | 729 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 10 | 8.414 | 0.8255 | 1.1673 | 42517 | 959 |

Overall: 21 model requests, latency p50 0.67 s / p95 1.174 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022347-s6_queue_priority-regular-three-rep0/`

### 20261029-022419-s6_queue_priority-regular-three-rep1 — s6_queue_priority × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.9 | 6 | 10.5 |
| Реализуйте stdev() | feature | completed | Verified successfully | 6.3 | 11 | 28.8 |

Bug round-trips:

- `765b0b98` Почините median() для чётной длины (activated 2026-10-28T23:24:27.514123+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 6.676 | 0.638 | 1.0164 | 28272 | 673 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 10 | 12.856 | 0.9205 | 3.2447 | 39315 | 992 |

Overall: 20 model requests, latency p50 0.7005 s / p95 1.5623 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022419-s6_queue_priority-regular-three-rep1/`

### 20261029-022419-s6_queue_priority-regular-three-rep2 — s6_queue_priority × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 4.6 | 10.8 | 29.3 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 5.4 | 8.2 | 13.2 |

Bug round-trips:

- `9c127375` Почините median() для чётной длины (activated 2026-10-28T23:24:27.537172+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 11 | 7.605 | 0.676 | 0.9265 | 32178 | 736 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 10 | 12.385 | 0.8275 | 3.1647 | 39295 | 1120 |

Overall: 21 model requests, latency p50 0.721 s / p95 1.49 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022419-s6_queue_priority-regular-three-rep2/`

### 20261029-022427-s6_queue_priority-regular-three-rep3 — s6_queue_priority × regular-three

Reason: `scenario failure: task 'test_stdev.py fails to collect: stdev() not implemented in stats.py' (abec360f) awaits clarification but no scenario answer matches: "The state is confirmed: test_stats.py green, ruff clean, and pytest . fails only because test_stdev.py imports a stdev() that doesn't exist yet in stats.py. How would you like to proceed?"`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | testing | — | 4.7 | 0.6 | — |
| Почините median() для чётной длины | bug | completed | Verified successfully | 3.6 | 10.9 | 14.1 |
| test_stdev.py fails to collect: stdev() not implemented in stats.py | bug | clarification | — | 11.8 | — | — |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:test_stdev.py fails to collect: stdev() not implemented in stats.py', 'tester': 'bug:Почините median() для чётной длины round 0', 'at': '2026-10-28T23:24:44.179526+00:00', 'detail': 'coder message at 2026-10-28T23:24:44.179526+00:00 inside tester interval 2026-10-28T23:24:35.545437+00:00…2026-10-28T23:24:45.986220+00:00'}

Bug round-trips:

- `70ddb4d9` Почините median() для чётной длины (activated 2026-10-28T23:24:31.393803+00:00)
- `abec360f` test_stdev.py fails to collect: stdev() not implemented in stats.py (activated 2026-10-28T23:24:46.760449+00:00)

User-simulator interventions: 0 (failure: 1, start: 1)
- SIM FAILURE: task 'test_stdev.py fails to collect: stdev() not implemented in stats.py' (abec360f) awaits clarification but no scenario answer matches: "The state is confirmed: test_stats.py green, ruff clean, and pytest . fails only because test_stdev.py imports a stdev() that doesn't exist yet in stats.py. How would you like to proceed?"

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 13.765 | 0.6885 | 3.2662 | 34776 | 1730 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 7.349 | 0.689 | 1.5748 | 30301 | 940 |

Overall: 20 model requests, latency p50 0.6885 s / p95 1.9238 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022427-s6_queue_priority-regular-three-rep3/`

### 20261029-022500-s6_queue_priority-regular-three-rep4 — s6_queue_priority × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 8.3 | 11 | 30.9 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 5.8 | 5.7 | 11.1 |

Bug round-trips:

- `c044f320` Почините median() для чётной длины (activated 2026-10-28T23:25:06.906089+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 11.625 | 0.545 | 2.279 | 38059 | 720 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 11 | 8.685 | 0.782 | 1.1035 | 42589 | 967 |

Overall: 24 model requests, latency p50 0.6905 s / p95 1.209 s.
Recorder ↔ transcript cross-check: 24/24 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022500-s6_queue_priority-regular-three-rep4/`

### 20261029-022500-s6_queue_priority-regular-three-rep5 — s6_queue_priority × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 5.5 | 11.4 | 16.5 |
| Реализуйте stdev() | feature | completed | Verified successfully | 4.9 | 9.8 | 32.2 |

Bug round-trips:

- `bf034957` Почините median() для чётной длины (activated 2026-10-28T23:25:06.905074+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 6.279 | 0.6355 | 0.8492 | 28350 | 600 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 13 | 9.945 | 0.67 | 1.2532 | 48636 | 1076 |

Overall: 23 model requests, latency p50 0.659 s / p95 1.171 s.
Recorder ↔ transcript cross-check: 23/23 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022500-s6_queue_priority-regular-three-rep5/`

### 20261029-022508-s6_queue_priority-regular-three-rep6 — s6_queue_priority × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 4.8 | 11.4 | 29.3 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 4 | 8.8 | 12.5 |

Bug round-trips:

- `f91cffd3` Почините median() для чётной длины (activated 2026-10-28T23:25:12.257835+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 6.803 | 0.686 | 1.14 | 26483 | 692 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 11 | 9.894 | 0.779 | 1.4925 | 44331 | 1286 |

Overall: 20 model requests, latency p50 0.7555 s / p95 1.3554 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022508-s6_queue_priority-regular-three-rep6/`

### 20261029-022541-s6_queue_priority-regular-three-rep7 — s6_queue_priority × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 4.9 | 11.2 | 28.6 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 4 | 8.4 | 12 |

Bug round-trips:

- `7066a64c` Почините median() для чётной длины (activated 2026-10-28T23:25:50.837233+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 6.166 | 0.759 | 0.888 | 25959 | 566 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 12 | 10.135 | 0.824 | 1.2965 | 48181 | 1206 |

Overall: 21 model requests, latency p50 0.779 s / p95 1.207 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022541-s6_queue_priority-regular-three-rep7/`

### 20261029-022543-s6_queue_priority-regular-three-rep8 — s6_queue_priority × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Реализуйте stdev() | feature | completed | Verified successfully | 4.4 | 8.9 | 26.6 |
| Почините median() для чётной длины | bug | completed | Verified successfully | 4 | 8.8 | 12.4 |

Bug round-trips:

- `c1321ab3` Почините median() для чётной длины (activated 2026-10-28T23:25:50.811260+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 5.505 | 0.6665 | 0.8801 | 22841 | 563 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 12 | 10.095 | 0.688 | 1.3277 | 44981 | 1154 |

Overall: 20 model requests, latency p50 0.688 s / p95 1.3013 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022543-s6_queue_priority-regular-three-rep8/`

### 20261029-022545-s6_queue_priority-regular-three-rep9 — s6_queue_priority × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Почините median() для чётной длины | bug | completed | Verified successfully | 4.6 | 8 | 12.3 |
| Реализуйте stdev() | feature | completed | Verified successfully | 4.7 | 7.1 | 24.9 |

Bug round-trips:

- `214c4dbb` Почините median() для чётной длины (activated 2026-10-28T23:25:50.827895+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 6.66 | 0.649 | 0.8566 | 28384 | 626 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 11 | 9.58 | 0.705 | 1.5885 | 42386 | 1253 |

Overall: 21 model requests, latency p50 0.682 s / p95 1.184 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022545-s6_queue_priority-regular-three-rep9/`

### 20261029-022813-s7_fault_injection-deepseek-v4-baseline-rep0 — s7_fault_injection × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 26 | 9.3 | 34.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@http://127.0.0.1:57947/p/copilot--deepseek-v4-flash-0731 | 8 | 16.696 | 1.999 | 2.9262 | 23947 | 673 |

Overall: 8 model requests, latency p50 1.999 s / p95 2.9262 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022813-s7_fault_injection-deepseek-v4-baseline-rep0/`

### 20261029-022814-s7_fault_injection-deepseek-v4-baseline-rep1 — s7_fault_injection × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 26.2 | 9.5 | 35.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@http://127.0.0.1:57950/p/copilot--deepseek-v4-flash-0731 | 8 | 17.174 | 2.144 | 3.0552 | 23918 | 706 |

Overall: 8 model requests, latency p50 2.144 s / p95 3.0552 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022814-s7_fault_injection-deepseek-v4-baseline-rep1/`

### 20261029-022851-s7_fault_injection-deepseek-v4-baseline-rep2 — s7_fault_injection × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 26 | 8.6 | 33.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@http://127.0.0.1:58097/p/copilot--deepseek-v4-flash-0731 | 8 | 15.67 | 1.8775 | 2.7333 | 23996 | 637 |

Overall: 8 model requests, latency p50 1.8775 s / p95 2.7333 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022851-s7_fault_injection-deepseek-v4-baseline-rep2/`

### 20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep3 — s7_fault_injection × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 26.6 | 16.1 | 39 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@http://127.0.0.1:58145/p/copilot--deepseek-v4-flash-0731 | 10 | 23.257 | 2.215 | 3.5156 | 30692 | 989 |

Overall: 10 model requests, latency p50 2.215 s / p95 3.5156 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep3/`

### 20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep4 — s7_fault_injection × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 26.4 | 15.1 | 41 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@http://127.0.0.1:58146/p/copilot--deepseek-v4-flash-0731 | 10 | 22.44 | 2.1135 | 3.1729 | 31756 | 907 |

Overall: 10 model requests, latency p50 2.1135 s / p95 3.1729 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022902-s7_fault_injection-deepseek-v4-baseline-rep4/`

### 20261029-022935-s7_fault_injection-deepseek-v4-baseline-rep5 — s7_fault_injection × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 27.6 | 21.5 | 48.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@http://127.0.0.1:58282/p/copilot--deepseek-v4-flash-0731 | 9 | 32.597 | 3.724 | 5.4546 | 30238 | 1070 |

Overall: 9 model requests, latency p50 3.724 s / p95 5.4546 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022935-s7_fault_injection-deepseek-v4-baseline-rep5/`

### 20261029-022954-s7_fault_injection-deepseek-v4-baseline-rep6 — s7_fault_injection × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 28.3 | 21.7 | 49.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@http://127.0.0.1:58344/p/copilot--deepseek-v4-flash-0731 | 10 | 29.805 | 2.9555 | 3.982 | 30709 | 873 |

Overall: 10 model requests, latency p50 2.9555 s / p95 3.982 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022954-s7_fault_injection-deepseek-v4-baseline-rep6/`

### 20261029-022955-s7_fault_injection-deepseek-v4-baseline-rep7 — s7_fault_injection × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 28.7 | 16.4 | 44.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@http://127.0.0.1:58345/p/copilot--deepseek-v4-flash-0731 | 9 | 26.471 | 2.933 | 3.696 | 27255 | 757 |

Overall: 9 model requests, latency p50 2.933 s / p95 3.696 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022955-s7_fault_injection-deepseek-v4-baseline-rep7/`

### 20261029-023040-s7_fault_injection-deepseek-v4-baseline-rep8 — s7_fault_injection × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 26.9 | 12.6 | 39 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@http://127.0.0.1:58517/p/copilot--deepseek-v4-flash-0731 | 9 | 19.453 | 2.135 | 2.7656 | 27340 | 795 |

Overall: 9 model requests, latency p50 2.135 s / p95 2.7656 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023040-s7_fault_injection-deepseek-v4-baseline-rep8/`

### 20261029-023049-s7_fault_injection-deepseek-v4-baseline-rep9 — s7_fault_injection × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 25.5 | 20.1 | 45 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@http://127.0.0.1:58547/p/copilot--deepseek-v4-flash-0731 | 10 | 26.677 | 2.605 | 3.5462 | 34551 | 1222 |

Overall: 10 model requests, latency p50 2.605 s / p95 3.5462 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023049-s7_fault_injection-deepseek-v4-baseline-rep9/`

### 20261029-022619-s7_fault_injection-glm-5.3-baseline-rep0 — s7_fault_injection × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 22.6 | 5 | 27.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:57492/p/copilot--glm-5.3-flash | 9 | 5.95 | 0.643 | 0.82 | 25996 | 399 |

Overall: 9 model requests, latency p50 0.643 s / p95 0.82 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022619-s7_fault_injection-glm-5.3-baseline-rep0/`

### 20261029-022620-s7_fault_injection-glm-5.3-baseline-rep1 — s7_fault_injection × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 22.6 | 6.2 | 28.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:57491/p/copilot--glm-5.3-flash | 10 | 7.127 | 0.7025 | 0.9974 | 32241 | 517 |

Overall: 10 model requests, latency p50 0.7025 s / p95 0.9974 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022620-s7_fault_injection-glm-5.3-baseline-rep1/`

### 20261029-022623-s7_fault_injection-glm-5.3-baseline-rep2 — s7_fault_injection × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 22 | 4.9 | 26.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:57501/p/copilot--glm-5.3-flash | 8 | 5.94 | 0.7015 | 1.1257 | 23345 | 484 |

Overall: 8 model requests, latency p50 0.7015 s / p95 1.1257 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022623-s7_fault_injection-glm-5.3-baseline-rep2/`

### 20261029-022657-s7_fault_injection-glm-5.3-baseline-rep3 — s7_fault_injection × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 23.2 | 5.1 | 27.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:57634/p/copilot--glm-5.3-flash | 8 | 6.135 | 0.7735 | 0.9894 | 22984 | 410 |

Overall: 8 model requests, latency p50 0.7735 s / p95 0.9894 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022657-s7_fault_injection-glm-5.3-baseline-rep3/`

### 20261029-022659-s7_fault_injection-glm-5.3-baseline-rep4 — s7_fault_injection × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 23.3 | 4.8 | 27.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:57638/p/copilot--glm-5.3-flash | 8 | 5.988 | 0.7125 | 1.0198 | 23384 | 442 |

Overall: 8 model requests, latency p50 0.7125 s / p95 1.0198 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022659-s7_fault_injection-glm-5.3-baseline-rep4/`

### 20261029-022700-s7_fault_injection-glm-5.3-baseline-rep5 — s7_fault_injection × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 23.1 | 5.3 | 28 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:57642/p/copilot--glm-5.3-flash | 8 | 6.215 | 0.813 | 0.9364 | 24071 | 408 |

Overall: 8 model requests, latency p50 0.813 s / p95 0.9364 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022700-s7_fault_injection-glm-5.3-baseline-rep5/`

### 20261029-022737-s7_fault_injection-glm-5.3-baseline-rep6 — s7_fault_injection × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 22.7 | 7.7 | 29.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:57792/p/copilot--glm-5.3-flash | 11 | 9.029 | 0.686 | 1.252 | 35986 | 747 |

Overall: 11 model requests, latency p50 0.686 s / p95 1.252 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022737-s7_fault_injection-glm-5.3-baseline-rep6/`

### 20261029-022737-s7_fault_injection-glm-5.3-baseline-rep7 — s7_fault_injection × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 22.4 | 6.5 | 28.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:57790/p/copilot--glm-5.3-flash | 11 | 7.777 | 0.673 | 1.0855 | 36036 | 664 |

Overall: 11 model requests, latency p50 0.673 s / p95 1.0855 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022737-s7_fault_injection-glm-5.3-baseline-rep7/`

### 20261029-022737-s7_fault_injection-glm-5.3-baseline-rep8 — s7_fault_injection × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 22.5 | 6.2 | 28.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:57791/p/copilot--glm-5.3-flash | 10 | 7.727 | 0.7015 | 1.1067 | 32162 | 473 |

Overall: 10 model requests, latency p50 0.7015 s / p95 1.1067 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022737-s7_fault_injection-glm-5.3-baseline-rep8/`

### 20261029-022812-s7_fault_injection-glm-5.3-baseline-rep9 — s7_fault_injection × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 23 | 4.1 | 26.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:57946/p/copilot--glm-5.3-flash | 8 | 5.376 | 0.635 | 0.8795 | 23058 | 510 |

Overall: 8 model requests, latency p50 0.635 s / p95 0.8795 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-022812-s7_fault_injection-glm-5.3-baseline-rep9/`

### 20261029-023055-s7_fault_injection-incredible-four-rep0 — s7_fault_injection × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.5 | 17.2 | 38 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:58575/p/copilot--glm-5.3-flash | 4 | 2.879 | 0.7165 | 0.889 | 11237 | 174 |
| x5-airun-medium-thinking@http://127.0.0.1:58575/p/copilot--qwen3.8-27b | 7 | 15.521 | 1.312 | 4.9541 | 34478 | 2394 |

Overall: 11 model requests, latency p50 0.913 s / p95 4.5135 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023055-s7_fault_injection-incredible-four-rep0/`

### 20261029-023131-s7_fault_injection-incredible-four-rep1 — s7_fault_injection × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 22.7 | 16.3 | 38.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:58711/p/copilot--glm-5.3-flash | 4 | 2.896 | 0.747 | 0.8511 | 11281 | 200 |
| x5-airun-medium-thinking@http://127.0.0.1:58711/p/copilot--qwen3.8-27b | 6 | 14.415 | 1.852 | 4.6928 | 29546 | 2306 |

Overall: 10 model requests, latency p50 1.163 s / p95 4.3229 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023131-s7_fault_injection-incredible-four-rep1/`

### 20261029-023141-s7_fault_injection-incredible-four-rep2 — s7_fault_injection × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.5 | 11.7 | 32.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:58751/p/copilot--glm-5.3-flash | 4 | 2.794 | 0.7575 | 0.7734 | 11272 | 191 |
| x5-airun-medium-thinking@http://127.0.0.1:58751/p/copilot--qwen3.8-27b | 6 | 9.289 | 1.268 | 2.942 | 25468 | 1199 |

Overall: 10 model requests, latency p50 0.914 s / p95 2.5636 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023141-s7_fault_injection-incredible-four-rep2/`

### 20261029-023143-s7_fault_injection-incredible-four-rep3 — s7_fault_injection × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.7 | 12.8 | 34.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:58756/p/copilot--glm-5.3-flash | 4 | 2.881 | 0.8065 | 0.8295 | 11393 | 193 |
| x5-airun-medium-thinking@http://127.0.0.1:58756/p/copilot--qwen3.8-27b | 6 | 11.222 | 2.032 | 2.6765 | 28025 | 1663 |

Overall: 10 model requests, latency p50 1.1095 s / p95 2.5561 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023143-s7_fault_injection-incredible-four-rep3/`

### 20261029-023218-s7_fault_injection-incredible-four-rep4 — s7_fault_injection × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.3 | 10.6 | 31.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:58895/p/copilot--glm-5.3-flash | 4 | 2.687 | 0.7365 | 0.7735 | 11272 | 196 |
| x5-airun-medium-thinking@http://127.0.0.1:58895/p/copilot--qwen3.8-27b | 6 | 9.274 | 1.3475 | 2.5735 | 24186 | 1437 |

Overall: 10 model requests, latency p50 1.0515 s / p95 2.3491 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023218-s7_fault_injection-incredible-four-rep4/`

### 20261029-023225-s7_fault_injection-incredible-four-rep5 — s7_fault_injection × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.2 | 11.2 | 32 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:58925/p/copilot--glm-5.3-flash | 4 | 2.621 | 0.674 | 0.7269 | 11257 | 190 |
| x5-airun-medium-thinking@http://127.0.0.1:58925/p/copilot--qwen3.8-27b | 6 | 8.153 | 1.095 | 2.2642 | 26256 | 1250 |

Overall: 10 model requests, latency p50 0.887 s / p95 2.15 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023225-s7_fault_injection-incredible-four-rep5/`

### 20261029-023227-s7_fault_injection-incredible-four-rep6 — s7_fault_injection × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.2 | 12.4 | 33.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:58934/p/copilot--glm-5.3-flash | 4 | 2.668 | 0.73 | 0.7677 | 11276 | 192 |
| x5-airun-medium-thinking@http://127.0.0.1:58934/p/copilot--qwen3.8-27b | 7 | 11.319 | 1.813 | 2.3682 | 28545 | 1738 |

Overall: 11 model requests, latency p50 0.774 s / p95 2.353 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023227-s7_fault_injection-incredible-four-rep6/`

### 20261029-023257-s7_fault_injection-incredible-four-rep7 — s7_fault_injection × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 22.1 | 10.1 | 31.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59064/p/copilot--glm-5.3-flash | 4 | 2.867 | 0.763 | 0.7978 | 11276 | 198 |
| x5-airun-medium-thinking@http://127.0.0.1:59064/p/copilot--qwen3.8-27b | 5 | 8.671 | 1.222 | 3.232 | 20475 | 1382 |

Overall: 9 model requests, latency p50 0.803 s / p95 2.927 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023257-s7_fault_injection-incredible-four-rep7/`

### 20261029-023305-s7_fault_injection-incredible-four-rep8 — s7_fault_injection × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.7 | 10.6 | 31.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59085/p/copilot--glm-5.3-flash | 4 | 2.606 | 0.6795 | 0.7779 | 11272 | 192 |
| x5-airun-medium-thinking@http://127.0.0.1:59085/p/copilot--qwen3.8-27b | 7 | 8.669 | 1.035 | 1.9379 | 28362 | 1218 |

Overall: 11 model requests, latency p50 0.829 s / p95 1.9305 s.
Recorder ↔ transcript cross-check: 11/11 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023305-s7_fault_injection-incredible-four-rep8/`

### 20261029-023308-s7_fault_injection-incredible-four-rep9 — s7_fault_injection × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.5 | 9.7 | 30.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59096/p/copilot--glm-5.3-flash | 4 | 2.646 | 0.68 | 0.8052 | 11257 | 194 |
| x5-airun-medium-thinking@http://127.0.0.1:59096/p/copilot--qwen3.8-27b | 5 | 7.745 | 1.262 | 2.8642 | 20600 | 1020 |

Overall: 9 model requests, latency p50 0.819 s / p95 2.4994 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023308-s7_fault_injection-incredible-four-rep9/`

### 20261029-023342-s7_fault_injection-regular-three-rep0 — s7_fault_injection × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 22.7 | 4.6 | 27 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59224/p/copilot--glm-5.3-flash | 4 | 2.781 | 0.7395 | 0.8252 | 11261 | 196 |
| x5-airun-medium@http://127.0.0.1:59224/p/copilot--qwen3.8-27b-noth | 4 | 2.776 | 0.6595 | 0.8554 | 14487 | 277 |

Overall: 8 model requests, latency p50 0.693 s / p95 0.8638 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023342-s7_fault_injection-regular-three-rep0/`

### 20261029-023345-s7_fault_injection-regular-three-rep1 — s7_fault_injection × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.1 | 6.3 | 26.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59241/p/copilot--glm-5.3-flash | 4 | 2.542 | 0.662 | 0.7129 | 11219 | 163 |
| x5-airun-medium@http://127.0.0.1:59241/p/copilot--qwen3.8-27b-noth | 6 | 4.241 | 0.6315 | 0.9502 | 20275 | 417 |

Overall: 10 model requests, latency p50 0.645 s / p95 0.9336 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023345-s7_fault_injection-regular-three-rep1/`

### 20261029-023348-s7_fault_injection-regular-three-rep2 — s7_fault_injection × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.3 | 5.2 | 26.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59254/p/copilot--glm-5.3-flash | 4 | 2.679 | 0.736 | 0.7677 | 11261 | 199 |
| x5-airun-medium@http://127.0.0.1:59254/p/copilot--qwen3.8-27b-noth | 5 | 2.874 | 0.598 | 0.7128 | 15625 | 303 |

Overall: 9 model requests, latency p50 0.62 s / p95 0.7622 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023348-s7_fault_injection-regular-three-rep2/`

### 20261029-023417-s7_fault_injection-regular-three-rep3 — s7_fault_injection × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 22.9 | 5.2 | 27.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59375/p/copilot--glm-5.3-flash | 4 | 3.228 | 0.794 | 1.0102 | 11261 | 211 |
| x5-airun-medium@http://127.0.0.1:59375/p/copilot--qwen3.8-27b-noth | 5 | 3.064 | 0.625 | 0.835 | 15560 | 342 |

Overall: 9 model requests, latency p50 0.643 s / p95 0.9772 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023417-s7_fault_injection-regular-three-rep3/`

### 20261029-023421-s7_fault_injection-regular-three-rep4 — s7_fault_injection × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.9 | 5 | 26.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59381/p/copilot--glm-5.3-flash | 4 | 2.862 | 0.7255 | 0.9384 | 11261 | 194 |
| x5-airun-medium@http://127.0.0.1:59381/p/copilot--qwen3.8-27b-noth | 4 | 2.995 | 0.757 | 0.9545 | 12222 | 270 |

Overall: 8 model requests, latency p50 0.7255 s / p95 0.9712 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023421-s7_fault_injection-regular-three-rep4/`

### 20261029-023422-s7_fault_injection-regular-three-rep5 — s7_fault_injection × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.7 | 6.3 | 27.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59383/p/copilot--glm-5.3-flash | 4 | 2.864 | 0.701 | 0.9392 | 11261 | 206 |
| x5-airun-medium@http://127.0.0.1:59383/p/copilot--qwen3.8-27b-noth | 6 | 3.982 | 0.663 | 0.8105 | 22059 | 380 |

Overall: 10 model requests, latency p50 0.693 s / p95 0.9137 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023422-s7_fault_injection-regular-three-rep5/`

### 20261029-023458-s7_fault_injection-regular-three-rep6 — s7_fault_injection × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 23.9 | 5 | 28.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59516/p/copilot--glm-5.3-flash | 5 | 3.581 | 0.723 | 0.8108 | 14259 | 253 |
| x5-airun-medium@http://127.0.0.1:59516/p/copilot--qwen3.8-27b-noth | 5 | 3.396 | 0.672 | 0.9704 | 15814 | 379 |

Overall: 10 model requests, latency p50 0.708 s / p95 0.9365 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023458-s7_fault_injection-regular-three-rep6/`

### 20261029-023458-s7_fault_injection-regular-three-rep7 — s7_fault_injection × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 23.3 | 5.1 | 28 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59517/p/copilot--glm-5.3-flash | 4 | 2.92 | 0.773 | 0.8432 | 11397 | 191 |
| x5-airun-medium@http://127.0.0.1:59517/p/copilot--qwen3.8-27b-noth | 5 | 3.047 | 0.546 | 0.7636 | 17632 | 246 |

Overall: 9 model requests, latency p50 0.682 s / p95 0.827 s.
Recorder ↔ transcript cross-check: 9/9 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023458-s7_fault_injection-regular-three-rep7/`

### 20261029-023459-s7_fault_injection-regular-three-rep8 — s7_fault_injection × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 23 | 5.9 | 28.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59521/p/copilot--glm-5.3-flash | 4 | 2.533 | 0.6635 | 0.7762 | 11276 | 180 |
| x5-airun-medium@http://127.0.0.1:59521/p/copilot--qwen3.8-27b-noth | 6 | 3.604 | 0.577 | 0.7275 | 19428 | 309 |

Overall: 10 model requests, latency p50 0.6455 s / p95 0.7711 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023459-s7_fault_injection-regular-three-rep8/`

### 20261029-023536-s7_fault_injection-regular-three-rep9 — s7_fault_injection × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Сделайте тест зелёным (bullet_list) | feature | completed | Verified successfully | 21.9 | 5.8 | 27.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@http://127.0.0.1:59672/p/copilot--glm-5.3-flash | 4 | 3.175 | 0.787 | 1.0352 | 11261 | 193 |
| x5-airun-medium@http://127.0.0.1:59672/p/copilot--qwen3.8-27b-noth | 6 | 3.644 | 0.5695 | 0.7978 | 22054 | 313 |

Overall: 10 model requests, latency p50 0.656 s / p95 0.9677 s.
Recorder ↔ transcript cross-check: 10/10 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023536-s7_fault_injection-regular-three-rep9/`

### 20261029-023744-s8_fix_loop-deepseek-v4-baseline-rep0 — s8_fix_loop × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 15.2 | 32.4 | 108.4 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:38:45.793620+00:00', 'detail': 'coder message at 2026-10-28T23:38:45.793620+00:00 inside tester interval 2026-10-28T23:38:06.374049+00:00…2026-10-28T23:38:46.504792+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 21 | 100.621 | 3.635 | 11.312 | 87067 | 4913 |

Overall: 21 model requests, latency p50 3.635 s / p95 11.312 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023744-s8_fix_loop-deepseek-v4-baseline-rep0/`

### 20261029-023806-s8_fix_loop-deepseek-v4-baseline-rep1 — s8_fix_loop × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 12.4 | 17.6 | 88.4 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:39:08.604342+00:00', 'detail': 'coder message at 2026-10-28T23:39:08.604342+00:00 inside tester interval 2026-10-28T23:38:36.730484+00:00…2026-10-28T23:39:09.100657+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 18 | 79.982 | 2.8075 | 9.3828 | 71429 | 3939 |

Overall: 18 model requests, latency p50 2.8075 s / p95 9.3828 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023806-s8_fix_loop-deepseek-v4-baseline-rep1/`

### 20261029-023810-s8_fix_loop-deepseek-v4-baseline-rep2 — s8_fix_loop × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 11.6 | 41.6 | 125.1 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:39:22.957861+00:00', 'detail': 'coder message at 2026-10-28T23:39:22.957861+00:00 inside tester interval 2026-10-28T23:38:37.914244+00:00…2026-10-28T23:39:23.455441+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 22 | 115.853 | 3.5835 | 16.7819 | 93054 | 5624 |

Overall: 22 model requests, latency p50 3.5835 s / p95 16.7819 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023810-s8_fix_loop-deepseek-v4-baseline-rep2/`

### 20261029-023939-s8_fix_loop-deepseek-v4-baseline-rep3 — s8_fix_loop × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 12.4 | 24.5 | 133.7 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:41:19.255131+00:00', 'detail': 'coder message at 2026-10-28T23:41:19.255131+00:00 inside tester interval 2026-10-28T23:40:20.022263+00:00…2026-10-28T23:41:19.839387+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 21 | 124.196 | 4.09 | 15.442 | 86141 | 6139 |

Overall: 21 model requests, latency p50 4.09 s / p95 15.442 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023939-s8_fix_loop-deepseek-v4-baseline-rep3/`

### 20261029-023947-s8_fix_loop-deepseek-v4-baseline-rep4 — s8_fix_loop × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 8.8 | 22.1 | 116.6 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:41:12.771213+00:00', 'detail': 'coder message at 2026-10-28T23:41:12.771213+00:00 inside tester interval 2026-10-28T23:40:13.077506+00:00…2026-10-28T23:41:13.599646+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 19 | 110.015 | 4.32 | 18.832 | 79185 | 5240 |

Overall: 19 model requests, latency p50 4.32 s / p95 18.832 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023947-s8_fix_loop-deepseek-v4-baseline-rep4/`

### 20261029-024026-s8_fix_loop-deepseek-v4-baseline-rep5 — s8_fix_loop × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 13.5 | 15.8 | 224.9 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:43:40.415782+00:00', 'detail': 'coder message at 2026-10-28T23:43:40.415782+00:00 inside tester interval 2026-10-28T23:40:49.363441+00:00…2026-10-28T23:43:41.160767+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 30 | 219.249 | 3.2485 | 22.0184 | 148220 | 11626 |

Overall: 30 model requests, latency p50 3.2485 s / p95 22.0184 s.
Recorder ↔ transcript cross-check: 30/30 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024026-s8_fix_loop-deepseek-v4-baseline-rep5/`

### 20261029-024154-s8_fix_loop-deepseek-v4-baseline-rep6 — s8_fix_loop × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 24.3 | 50.5 | 186.4 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:43:48.414367+00:00', 'detail': 'coder message at 2026-10-28T23:43:48.414367+00:00 inside tester interval 2026-10-28T23:42:24.999372+00:00…2026-10-28T23:43:49.046717+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 22 | 178.891 | 3.316 | 28.7673 | 92289 | 9816 |

Overall: 22 model requests, latency p50 3.316 s / p95 28.7673 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024154-s8_fix_loop-deepseek-v4-baseline-rep6/`

### 20261029-024205-s8_fix_loop-deepseek-v4-baseline-rep7 — s8_fix_loop × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 16.7 | 18 | 89.3 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:42:59.606451+00:00', 'detail': 'coder message at 2026-10-28T23:42:59.606451+00:00 inside tester interval 2026-10-28T23:42:22.295975+00:00…2026-10-28T23:43:00.241470+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 19 | 81.369 | 2.449 | 12.4414 | 76185 | 4110 |

Overall: 19 model requests, latency p50 2.449 s / p95 12.4414 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024205-s8_fix_loop-deepseek-v4-baseline-rep7/`

### 20261029-024346-s8_fix_loop-deepseek-v4-baseline-rep8 — s8_fix_loop × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 31.2 | 29.9 | 119.9 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:44:47.767827+00:00', 'detail': 'coder message at 2026-10-28T23:44:47.767827+00:00 inside tester interval 2026-10-28T23:44:16.298236+00:00…2026-10-28T23:44:48.994555+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 21 | 113.657 | 4.083 | 17.14 | 134632 | 5784 |

Overall: 21 model requests, latency p50 4.083 s / p95 17.14 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024346-s8_fix_loop-deepseek-v4-baseline-rep8/`

### 20261029-024422-s8_fix_loop-deepseek-v4-baseline-rep9 — s8_fix_loop × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 17.1 | 17.3 | 102.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:45:30.355453+00:00', 'detail': 'coder message at 2026-10-28T23:45:30.355453+00:00 inside tester interval 2026-10-28T23:44:49.984979+00:00…2026-10-28T23:45:31.295333+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 22 | 95.153 | 2.975 | 12.1017 | 96624 | 4888 |

Overall: 22 model requests, latency p50 2.975 s / p95 12.1017 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024422-s8_fix_loop-deepseek-v4-baseline-rep9/`

### 20261029-023536-s8_fix_loop-glm-5.3-baseline-rep0 — s8_fix_loop × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.5 | 5.3 | 26.8 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:36:01.213745+00:00', 'detail': 'coder message at 2026-10-28T23:36:01.213745+00:00 inside tester interval 2026-10-28T23:35:51.768811+00:00…2026-10-28T23:36:01.896692+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 17 | 17.096 | 0.876 | 1.935 | 69796 | 2434 |

Overall: 17 model requests, latency p50 0.876 s / p95 1.935 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023536-s8_fix_loop-glm-5.3-baseline-rep0/`

### 20261029-023538-s8_fix_loop-glm-5.3-baseline-rep1 — s8_fix_loop × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 4.9 | 7.6 | 28.4 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:35:59.250656+00:00', 'detail': 'coder message at 2026-10-28T23:35:59.250656+00:00 inside tester interval 2026-10-28T23:35:51.847456+00:00…2026-10-28T23:35:59.682258+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 20 | 19.242 | 0.7215 | 1.6866 | 78706 | 2705 |

Overall: 20 model requests, latency p50 0.7215 s / p95 1.6866 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023538-s8_fix_loop-glm-5.3-baseline-rep1/`

### 20261029-023614-s8_fix_loop-glm-5.3-baseline-rep2 — s8_fix_loop × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 5.9 | 5.4 | 28.6 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:36:35.439544+00:00', 'detail': 'coder message at 2026-10-28T23:36:35.439544+00:00 inside tester interval 2026-10-28T23:36:28.927084+00:00…2026-10-28T23:36:36.338980+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 19 | 20.283 | 0.947 | 1.7761 | 78926 | 2887 |

Overall: 19 model requests, latency p50 0.947 s / p95 1.7761 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023614-s8_fix_loop-glm-5.3-baseline-rep2/`

### 20261029-023614-s8_fix_loop-glm-5.3-baseline-rep3 — s8_fix_loop × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 5.1 | 10.1 | 32.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:36:35.652005+00:00', 'detail': 'coder message at 2026-10-28T23:36:35.652005+00:00 inside tester interval 2026-10-28T23:36:27.948208+00:00…2026-10-28T23:36:36.183636+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 17 | 21.552 | 1.112 | 2.4042 | 70754 | 3106 |

Overall: 17 model requests, latency p50 1.112 s / p95 2.4042 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023614-s8_fix_loop-glm-5.3-baseline-rep3/`

### 20261029-023617-s8_fix_loop-glm-5.3-baseline-rep4 — s8_fix_loop × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 4.2 | 6.9 | 28.4 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:36:37.192588+00:00', 'detail': 'coder message at 2026-10-28T23:36:37.192588+00:00 inside tester interval 2026-10-28T23:36:29.308261+00:00…2026-10-28T23:36:37.665239+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 17 | 18.047 | 0.892 | 1.9238 | 66241 | 2169 |

Overall: 17 model requests, latency p50 0.892 s / p95 1.9238 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023617-s8_fix_loop-glm-5.3-baseline-rep4/`

### 20261029-023651-s8_fix_loop-glm-5.3-baseline-rep5 — s8_fix_loop × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 4.5 | 8.6 | 28 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:37:16.111739+00:00', 'detail': 'coder message at 2026-10-28T23:37:16.111739+00:00 inside tester interval 2026-10-28T23:37:09.624469+00:00…2026-10-28T23:37:16.551884+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 16 | 20.144 | 1.2185 | 2.316 | 63128 | 2456 |

Overall: 16 model requests, latency p50 1.2185 s / p95 2.316 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023651-s8_fix_loop-glm-5.3-baseline-rep5/`

### 20261029-023652-s8_fix_loop-glm-5.3-baseline-rep6 — s8_fix_loop × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 6.5 | 12.2 | 33.4 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:37:16.190203+00:00', 'detail': 'coder message at 2026-10-28T23:37:16.190203+00:00 inside tester interval 2026-10-28T23:37:10.515512+00:00…2026-10-28T23:37:16.598117+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 19 | 24.875 | 0.886 | 2.4699 | 76017 | 2737 |

Overall: 19 model requests, latency p50 0.886 s / p95 2.4699 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023652-s8_fix_loop-glm-5.3-baseline-rep6/`

### 20261029-023655-s8_fix_loop-glm-5.3-baseline-rep7 — s8_fix_loop × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 12.5 | 11.7 | 38.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:37:15.189801+00:00', 'detail': 'coder message at 2026-10-28T23:37:15.189801+00:00 inside tester interval 2026-10-28T23:37:09.715702+00:00…2026-10-28T23:37:15.684458+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 19 | 29.59 | 1.367 | 3.0003 | 76038 | 2761 |

Overall: 19 model requests, latency p50 1.367 s / p95 3.0003 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023655-s8_fix_loop-glm-5.3-baseline-rep7/`

### 20261029-023734-s8_fix_loop-glm-5.3-baseline-rep8 — s8_fix_loop × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.8 | 6.9 | 23.3 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:37:50.405232+00:00', 'detail': 'coder message at 2026-10-28T23:37:50.405232+00:00 inside tester interval 2026-10-28T23:37:45.317780+00:00…2026-10-28T23:37:50.899521+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 15 | 16.864 | 1.019 | 2.1361 | 58046 | 2414 |

Overall: 15 model requests, latency p50 1.019 s / p95 2.1361 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023734-s8_fix_loop-glm-5.3-baseline-rep8/`

### 20261029-023739-s8_fix_loop-glm-5.3-baseline-rep9 — s8_fix_loop × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.8 | 5.3 | 23.8 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:37:56.810397+00:00', 'detail': 'coder message at 2026-10-28T23:37:56.810397+00:00 inside tester interval 2026-10-28T23:37:50.600163+00:00…2026-10-28T23:37:57.335611+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 16 | 15.926 | 0.8615 | 1.8118 | 63107 | 2219 |

Overall: 16 model requests, latency p50 0.8615 s / p95 1.8118 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-023739-s8_fix_loop-glm-5.3-baseline-rep9/`

### 20261029-024513-s8_fix_loop-incredible-four-rep0 — s8_fix_loop × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 5.9 | 23 | 58.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:45:50.254516+00:00', 'detail': 'coder message at 2026-10-28T23:45:50.254516+00:00 inside tester interval 2026-10-28T23:45:31.391759+00:00…2026-10-28T23:45:50.945562+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 9.908 | 0.837 | 1.9294 | 41353 | 1288 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 17 | 37.515 | 1.828 | 3.8382 | 101300 | 6174 |

Overall: 27 model requests, latency p50 1.489 s / p95 3.7848 s.
Recorder ↔ transcript cross-check: 27/27 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024513-s8_fix_loop-incredible-four-rep0/`

### 20261029-024601-s8_fix_loop-incredible-four-rep1 — s8_fix_loop × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 4.5 | 22.7 | 55.1 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:46:30.264569+00:00', 'detail': 'coder message at 2026-10-28T23:46:30.264569+00:00 inside tester interval 2026-10-28T23:46:12.994121+00:00…2026-10-28T23:46:30.997081+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 8.61 | 0.7295 | 2.2411 | 32842 | 1477 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 15 | 37.46 | 2.33 | 4.1454 | 88180 | 6326 |

Overall: 23 model requests, latency p50 1.909 s / p95 3.883 s.
Recorder ↔ transcript cross-check: 23/23 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024601-s8_fix_loop-incredible-four-rep1/`

### 20261029-024614-s8_fix_loop-incredible-four-rep2 — s8_fix_loop × incredible-four

Reason: `settled but checks.py failed:
S8 checks FAILED:
- task b2dca36d: fix-loop requeue event found 0 times in events, expected exactly 1 (event: 'testing failed — returned for another development round (round 2/3)')
- task b2dca36d: 1 testing rounds, expected >= 2 (the round after the fix-loop requeue is missing)
- task b2dca36d: 1 development rounds (user prompts), expected >= 2 (the tester's report must reach the coder as the task's next input)`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 16.9 | 22.4 | 38.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 10.096 | 0.953 | 1.7899 | 43085 | 1154 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 18.36 | 1.932 | 3.8751 | 47746 | 2768 |

Overall: 18 model requests, latency p50 1.1785 s / p95 3.5781 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024614-s8_fix_loop-incredible-four-rep2/`

### 20261029-024626-s8_fix_loop-incredible-four-rep3 — s8_fix_loop × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 6.4 | 23 | 60.2 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:47:01.919334+00:00', 'detail': 'coder message at 2026-10-28T23:47:01.919334+00:00 inside tester interval 2026-10-28T23:46:41.964052+00:00…2026-10-28T23:47:02.630207+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 11 | 10.769 | 0.679 | 2.411 | 47069 | 1355 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 37.631 | 2.131 | 4.2832 | 91265 | 6117 |

Overall: 27 model requests, latency p50 1.497 s / p95 4.1146 s.
Recorder ↔ transcript cross-check: 27/27 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024626-s8_fix_loop-incredible-four-rep3/`

### 20261029-024703-s8_fix_loop-incredible-four-rep4 — s8_fix_loop × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 4.9 | 13.6 | 53.7 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:47:40.631302+00:00', 'detail': 'coder message at 2026-10-28T23:47:40.631302+00:00 inside tester interval 2026-10-28T23:47:16.469750+00:00…2026-10-28T23:47:41.613949+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 10.209 | 0.8355 | 2.0369 | 42889 | 1533 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 14 | 33.37 | 1.958 | 4.7184 | 122664 | 4925 |

Overall: 24 model requests, latency p50 1.701 s / p95 4.289 s.
Recorder ↔ transcript cross-check: 24/24 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024703-s8_fix_loop-incredible-four-rep4/`

### 20261029-024704-s8_fix_loop-incredible-four-rep5 — s8_fix_loop × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 8.7 | 23 | 105 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:48:18.823657+00:00', 'detail': 'coder message at 2026-10-28T23:48:18.823657+00:00 inside tester interval 2026-10-28T23:47:15.802585+00:00…2026-10-28T23:48:19.702951+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 10.598 | 0.8595 | 2.1732 | 46872 | 1714 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 18 | 82.011 | 4.0205 | 10.6559 | 169467 | 13455 |

Overall: 28 model requests, latency p50 2.063 s / p95 9.2399 s.
Recorder ↔ transcript cross-check: 28/28 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024704-s8_fix_loop-incredible-four-rep5/`

### 20261029-024737-s8_fix_loop-incredible-four-rep6 — s8_fix_loop × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.9 | 19.4 | 59.8 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:48:20.976472+00:00', 'detail': 'coder message at 2026-10-28T23:48:20.976472+00:00 inside tester interval 2026-10-28T23:47:54.335286+00:00…2026-10-28T23:48:21.699750+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 7.394 | 0.7875 | 1.5952 | 32497 | 1124 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 14 | 41.781 | 2.2725 | 6.8753 | 84396 | 7572 |

Overall: 22 model requests, latency p50 1.5935 s / p95 6.1136 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024737-s8_fix_loop-incredible-four-rep6/`

### 20261029-024805-s8_fix_loop-incredible-four-rep7 — s8_fix_loop × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 4.8 | 18.4 | 71.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:48:48.159814+00:00', 'detail': 'coder message at 2026-10-28T23:48:48.159814+00:00 inside tester interval 2026-10-28T23:48:16.982680+00:00…2026-10-28T23:48:53.650260+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 8.574 | 0.793 | 1.6116 | 37377 | 1224 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 15 | 53.685 | 3.813 | 6.4719 | 127472 | 8042 |

Overall: 24 model requests, latency p50 1.5905 s / p95 6.2403 s.
Recorder ↔ transcript cross-check: 24/24 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024805-s8_fix_loop-incredible-four-rep7/`

### 20261029-024851-s8_fix_loop-incredible-four-rep8 — s8_fix_loop × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.8 | 20.9 | 59.3 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:49:31.411932+00:00', 'detail': 'coder message at 2026-10-28T23:49:31.411932+00:00 inside tester interval 2026-10-28T23:49:07.219648+00:00…2026-10-28T23:49:33.071065+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 6.54 | 0.701 | 1.2506 | 31798 | 892 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 14 | 41.341 | 3.224 | 5.5264 | 115396 | 6565 |

Overall: 22 model requests, latency p50 1.411 s / p95 5.1221 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024851-s8_fix_loop-incredible-four-rep8/`

### 20261029-024859-s8_fix_loop-incredible-four-rep9 — s8_fix_loop × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.6 | 24.9 | 60.6 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:49:32.822697+00:00', 'detail': 'coder message at 2026-10-28T23:49:32.822697+00:00 inside tester interval 2026-10-28T23:49:09.242698+00:00…2026-10-28T23:49:33.451350+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 6.256 | 0.721 | 1.4269 | 28196 | 889 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 43.464 | 2.136 | 6.0732 | 91508 | 7178 |

Overall: 23 model requests, latency p50 1.531 s / p95 5.7688 s.
Recorder ↔ transcript cross-check: 23/23 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024859-s8_fix_loop-incredible-four-rep9/`

### 20261029-024925-s8_fix_loop-regular-three-rep0 — s8_fix_loop × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.2 | 5.1 | 23.9 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:49:45.060454+00:00', 'detail': 'coder message at 2026-10-28T23:49:45.060454+00:00 inside tester interval 2026-10-28T23:49:39.669300+00:00…2026-10-28T23:49:45.451992+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 7.155 | 0.772 | 1.2452 | 34613 | 782 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 9 | 7.652 | 0.739 | 1.439 | 34905 | 803 |

Overall: 18 model requests, latency p50 0.7555 s / p95 1.4623 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024925-s8_fix_loop-regular-three-rep0/`

### 20261029-024957-s8_fix_loop-regular-three-rep1 — s8_fix_loop × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 4.2 | 7.8 | 26 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:50:20.135127+00:00', 'detail': 'coder message at 2026-10-28T23:50:20.135127+00:00 inside tester interval 2026-10-28T23:50:14.470425+00:00…2026-10-28T23:50:20.475487+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 7.606 | 0.901 | 1.9779 | 28617 | 1151 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 13 | 10.408 | 0.611 | 1.6128 | 54127 | 1230 |

Overall: 20 model requests, latency p50 0.7425 s / p95 2.1724 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-024957-s8_fix_loop-regular-three-rep1/`

### 20261029-025003-s8_fix_loop-regular-three-rep2 — s8_fix_loop × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 4.1 | 5.7 | 25.1 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:50:21.775631+00:00', 'detail': 'coder message at 2026-10-28T23:50:21.775631+00:00 inside tester interval 2026-10-28T23:50:16.030546+00:00…2026-10-28T23:50:22.123743+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 8.243 | 0.87 | 1.321 | 36268 | 1090 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 9 | 9.126 | 0.793 | 2.0648 | 36396 | 1130 |

Overall: 18 model requests, latency p50 0.795 s / p95 1.6292 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025003-s8_fix_loop-regular-three-rep2/`

### 20261029-025008-s8_fix_loop-regular-three-rep3 — s8_fix_loop × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.5 | 5.8 | 23.4 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:50:24.979542+00:00', 'detail': 'coder message at 2026-10-28T23:50:24.979542+00:00 inside tester interval 2026-10-28T23:50:18.415225+00:00…2026-10-28T23:50:25.567844+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 5.827 | 0.605 | 1.5349 | 27509 | 805 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 11 | 9.956 | 0.758 | 1.8155 | 47808 | 1148 |

Overall: 18 model requests, latency p50 0.71 s / p95 1.8275 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025008-s8_fix_loop-regular-three-rep3/`

### 20261029-025036-s8_fix_loop-regular-three-rep4 — s8_fix_loop × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.2 | 6.4 | 25.3 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:50:55.566145+00:00', 'detail': 'coder message at 2026-10-28T23:50:55.566145+00:00 inside tester interval 2026-10-28T23:50:48.851297+00:00…2026-10-28T23:50:56.053129+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 6.844 | 0.687 | 1.216 | 35815 | 844 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 11 | 10.763 | 0.702 | 2.2195 | 45138 | 1242 |

Overall: 20 model requests, latency p50 0.6945 s / p95 1.7196 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025036-s8_fix_loop-regular-three-rep4/`

### 20261029-025036-s8_fix_loop-regular-three-rep5 — s8_fix_loop × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 4.3 | 13.1 | 39.6 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:51:01.475637+00:00', 'detail': 'coder message at 2026-10-28T23:51:01.475637+00:00 inside tester interval 2026-10-28T23:50:49.025148+00:00…2026-10-28T23:51:02.807308+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 8.69 | 0.6205 | 1.6553 | 40979 | 1311 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 18 | 21.639 | 1.0465 | 2.3938 | 128290 | 2620 |

Overall: 28 model requests, latency p50 0.9765 s / p95 2.2465 s.
Recorder ↔ transcript cross-check: 28/28 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025036-s8_fix_loop-regular-three-rep5/`

### 20261029-025038-s8_fix_loop-regular-three-rep6 — s8_fix_loop × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.2 | 7 | 23.9 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:50:54.589824+00:00', 'detail': 'coder message at 2026-10-28T23:50:54.589824+00:00 inside tester interval 2026-10-28T23:50:48.416975+00:00…2026-10-28T23:50:55.303388+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 5.153 | 0.68 | 1.0792 | 27182 | 704 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 10 | 10.574 | 0.801 | 1.9891 | 40201 | 1153 |

Overall: 17 model requests, latency p50 0.752 s / p95 1.9146 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025038-s8_fix_loop-regular-three-rep6/`

### 20261029-025110-s8_fix_loop-regular-three-rep7 — s8_fix_loop × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 5.5 | 6 | 27 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:51:33.309737+00:00', 'detail': 'coder message at 2026-10-28T23:51:33.309737+00:00 inside tester interval 2026-10-28T23:51:27.331543+00:00…2026-10-28T23:51:33.832237+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 8.565 | 0.9245 | 1.8353 | 31822 | 1126 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 10 | 9.198 | 0.6285 | 1.7871 | 39915 | 1015 |

Overall: 18 model requests, latency p50 0.711 s / p95 1.8315 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025110-s8_fix_loop-regular-three-rep7/`

### 20261029-025110-s8_fix_loop-regular-three-rep8 — s8_fix_loop × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 4.1 | 7.1 | 24.9 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:51:31.460273+00:00', 'detail': 'coder message at 2026-10-28T23:51:31.460273+00:00 inside tester interval 2026-10-28T23:51:25.735032+00:00…2026-10-28T23:51:31.832175+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 6.461 | 0.791 | 1.5107 | 28507 | 1071 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 12 | 9.998 | 0.6955 | 1.5966 | 51277 | 1185 |

Overall: 19 model requests, latency p50 0.712 s / p95 1.5482 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025110-s8_fix_loop-regular-three-rep8/`

### 20261029-025125-s8_fix_loop-regular-three-rep9 — s8_fix_loop × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Добавьте обрезку в pad() | feature | completed | Verified successfully | 3.3 | 6.1 | 23 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'feature:Добавьте обрезку в pad()', 'tester': 'feature:Добавьте обрезку в pad() round 0', 'at': '2026-10-28T23:51:42.910949+00:00', 'detail': 'coder message at 2026-10-28T23:51:42.910949+00:00 inside tester interval 2026-10-28T23:51:36.344542+00:00…2026-10-28T23:51:43.419686+00:00'}

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 5.296 | 0.621 | 1.2344 | 27214 | 684 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 12 | 10.445 | 0.7235 | 1.5516 | 50401 | 1161 |

Overall: 19 model requests, latency p50 0.7 s / p95 1.4438 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025125-s8_fix_loop-regular-three-rep9/`

### 20261029-025219-s9_research_count-deepseek-v4-baseline-rep0 — s9_research_count × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 10.6 | — | 13.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 12.181 | 3.047 | 3.1322 | 24274 | 536 |

Overall: 5 model requests, latency p50 3.047 s / p95 3.1322 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025219-s9_research_count-deepseek-v4-baseline-rep0/`

### 20261029-025229-s9_research_count-deepseek-v4-baseline-rep1 — s9_research_count × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 12.9 | — | 16.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 16.027 | 3.393 | 4.6982 | 24325 | 741 |

Overall: 5 model requests, latency p50 3.393 s / p95 4.6982 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025229-s9_research_count-deepseek-v4-baseline-rep1/`

### 20261029-025230-s9_research_count-deepseek-v4-baseline-rep2 — s9_research_count × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 17 | — | 20.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 19.681 | 3.879 | 4.7034 | 24601 | 975 |

Overall: 5 model requests, latency p50 3.879 s / p95 4.7034 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025230-s9_research_count-deepseek-v4-baseline-rep2/`

### 20261029-025238-s9_research_count-deepseek-v4-baseline-rep3 — s9_research_count × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 11.2 | — | 15 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 14.304 | 3.023 | 4.1854 | 24267 | 646 |

Overall: 5 model requests, latency p50 3.023 s / p95 4.1854 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025238-s9_research_count-deepseek-v4-baseline-rep3/`

### 20261029-025251-s9_research_count-deepseek-v4-baseline-rep4 — s9_research_count × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 15.6 | — | 17.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 17.107 | 4.053 | 4.4396 | 24476 | 762 |

Overall: 5 model requests, latency p50 4.053 s / p95 4.4396 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025251-s9_research_count-deepseek-v4-baseline-rep4/`

### 20261029-025255-s9_research_count-deepseek-v4-baseline-rep5 — s9_research_count × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 16.9 | — | 20.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 19.261 | 3.737 | 5.497 | 24629 | 868 |

Overall: 5 model requests, latency p50 3.737 s / p95 5.497 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025255-s9_research_count-deepseek-v4-baseline-rep5/`

### 20261029-025258-s9_research_count-deepseek-v4-baseline-rep6 — s9_research_count × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 8.6 | — | 12.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 11.884 | 1.987 | 3.8194 | 23991 | 479 |

Overall: 5 model requests, latency p50 1.987 s / p95 3.8194 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025258-s9_research_count-deepseek-v4-baseline-rep6/`

### 20261029-025315-s9_research_count-deepseek-v4-baseline-rep7 — s9_research_count × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 10.5 | — | 14.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 13.944 | 3.8205 | 4.2854 | 19211 | 627 |

Overall: 4 model requests, latency p50 3.8205 s / p95 4.2854 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025315-s9_research_count-deepseek-v4-baseline-rep7/`

### 20261029-025315-s9_research_count-deepseek-v4-baseline-rep8 — s9_research_count × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 8.4 | — | 11.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 10.798 | 2.695 | 3.5067 | 19185 | 463 |

Overall: 4 model requests, latency p50 2.695 s / p95 3.5067 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025315-s9_research_count-deepseek-v4-baseline-rep8/`

### 20261029-025320-s9_research_count-deepseek-v4-baseline-rep9 — s9_research_count × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 17.2 | — | 20.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 19.21 | 2.489 | 4.4987 | 35007 | 767 |

Overall: 7 model requests, latency p50 2.489 s / p95 4.4987 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025320-s9_research_count-deepseek-v4-baseline-rep9/`

### 20261029-025147-s9_research_count-glm-5.3-baseline-rep0 — s9_research_count × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 3 | — | 3.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 3.036 | 0.731 | 0.9583 | 18610 | 408 |

Overall: 4 model requests, latency p50 0.731 s / p95 0.9583 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025147-s9_research_count-glm-5.3-baseline-rep0/`

### 20261029-025149-s9_research_count-glm-5.3-baseline-rep1 — s9_research_count × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 3.7 | — | 4.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 3.462 | 0.681 | 0.8662 | 23723 | 392 |

Overall: 5 model requests, latency p50 0.681 s / p95 0.8662 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025149-s9_research_count-glm-5.3-baseline-rep1/`

### 20261029-025155-s9_research_count-glm-5.3-baseline-rep2 — s9_research_count × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 5.3 | — | 6.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 5.631 | 0.7815 | 1.7658 | 28380 | 495 |

Overall: 6 model requests, latency p50 0.7815 s / p95 1.7658 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025155-s9_research_count-glm-5.3-baseline-rep2/`

### 20261029-025157-s9_research_count-glm-5.3-baseline-rep3 — s9_research_count × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 5.2 | — | 6.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 5.917 | 0.835 | 1.7148 | 28434 | 451 |

Overall: 6 model requests, latency p50 0.835 s / p95 1.7148 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025157-s9_research_count-glm-5.3-baseline-rep3/`

### 20261029-025158-s9_research_count-glm-5.3-baseline-rep4 — s9_research_count × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 3.3 | — | 3.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 3.336 | 0.826 | 0.8875 | 18708 | 431 |

Overall: 4 model requests, latency p50 0.826 s / p95 0.8875 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025158-s9_research_count-glm-5.3-baseline-rep4/`

### 20261029-025207-s9_research_count-glm-5.3-baseline-rep5 — s9_research_count × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 3.1 | — | 3.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 3.193 | 0.8345 | 0.9698 | 18458 | 241 |

Overall: 4 model requests, latency p50 0.8345 s / p95 0.9698 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025207-s9_research_count-glm-5.3-baseline-rep5/`

### 20261029-025208-s9_research_count-glm-5.3-baseline-rep6 — s9_research_count × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 2.6 | — | 3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.78 | 0.737 | 0.7801 | 18726 | 319 |

Overall: 4 model requests, latency p50 0.737 s / p95 0.7801 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025208-s9_research_count-glm-5.3-baseline-rep6/`

### 20261029-025210-s9_research_count-glm-5.3-baseline-rep7 — s9_research_count × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 3.7 | — | 4.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 3.508 | 0.719 | 0.9412 | 23752 | 420 |

Overall: 5 model requests, latency p50 0.719 s / p95 0.9412 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025210-s9_research_count-glm-5.3-baseline-rep7/`

### 20261029-025216-s9_research_count-glm-5.3-baseline-rep8 — s9_research_count × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 4.6 | — | 5.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 4.06 | 0.582 | 0.979 | 28133 | 438 |

Overall: 6 model requests, latency p50 0.582 s / p95 0.979 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025216-s9_research_count-glm-5.3-baseline-rep8/`

### 20261029-025216-s9_research_count-glm-5.3-baseline-rep9 — s9_research_count × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 3.1 | — | 3.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 3.258 | 0.8485 | 0.9472 | 18888 | 404 |

Overall: 4 model requests, latency p50 0.8485 s / p95 0.9472 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025216-s9_research_count-glm-5.3-baseline-rep9/`

### 20261029-025331-s9_research_count-incredible-four-rep0 — s9_research_count × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 17.1 | — | 19.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 18.856 | 3.789 | 5.2632 | 24581 | 826 |

Overall: 5 model requests, latency p50 3.789 s / p95 5.2632 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025331-s9_research_count-incredible-four-rep0/`

### 20261029-025334-s9_research_count-incredible-four-rep1 — s9_research_count × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 9.6 | — | 12.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 12.01 | 3.233 | 3.5831 | 19213 | 550 |

Overall: 4 model requests, latency p50 3.233 s / p95 3.5831 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025334-s9_research_count-incredible-four-rep1/`

### 20261029-025349-s9_research_count-incredible-four-rep2 — s9_research_count × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 10.4 | — | 15.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 15.574 | 3.859 | 5.7311 | 19188 | 663 |

Overall: 4 model requests, latency p50 3.859 s / p95 5.7311 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025349-s9_research_count-incredible-four-rep2/`

### 20261029-025351-s9_research_count-incredible-four-rep3 — s9_research_count × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 12.7 | — | 16.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 16.185 | 4.4385 | 5.4124 | 19345 | 708 |

Overall: 4 model requests, latency p50 4.4385 s / p95 5.4124 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025351-s9_research_count-incredible-four-rep3/`

### 20261029-025356-s9_research_count-incredible-four-rep4 — s9_research_count × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 15.8 | — | 20.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 20.138 | 4.993 | 5.5734 | 24555 | 855 |

Overall: 5 model requests, latency p50 4.993 s / p95 5.5734 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025356-s9_research_count-incredible-four-rep4/`

### 20261029-025411-s9_research_count-incredible-four-rep5 — s9_research_count × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 13.6 | — | 16.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 16.573 | 4.418 | 5.8265 | 19188 | 542 |

Overall: 4 model requests, latency p50 4.418 s / p95 5.8265 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025411-s9_research_count-incredible-four-rep5/`

### 20261029-025413-s9_research_count-incredible-four-rep6 — s9_research_count × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 21.9 | — | 23.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 23.135 | 3.713 | 7.934 | 24446 | 816 |

Overall: 5 model requests, latency p50 3.713 s / p95 7.934 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025413-s9_research_count-incredible-four-rep6/`

### 20261029-025423-s9_research_count-incredible-four-rep7 — s9_research_count × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 10.8 | — | 14.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 13.948 | 3.7355 | 4.5605 | 19213 | 626 |

Overall: 4 model requests, latency p50 3.7355 s / p95 4.5605 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025423-s9_research_count-incredible-four-rep7/`

### 20261029-025433-s9_research_count-incredible-four-rep8 — s9_research_count × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 10.1 | — | 12.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 11.853 | 3.158 | 4.0641 | 19398 | 477 |

Overall: 4 model requests, latency p50 3.158 s / p95 4.0641 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025433-s9_research_count-incredible-four-rep8/`

### 20261029-025442-s9_research_count-incredible-four-rep9 — s9_research_count × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 16.8 | — | 21.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 20.754 | 3.584 | 8.7276 | 24304 | 715 |

Overall: 5 model requests, latency p50 3.584 s / p95 8.7276 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025442-s9_research_count-incredible-four-rep9/`

### 20261029-025446-s9_research_count-regular-three-rep0 — s9_research_count × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 4 | — | 4.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 3.878 | 0.732 | 1.0682 | 23856 | 438 |

Overall: 5 model requests, latency p50 0.732 s / p95 1.0682 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025446-s9_research_count-regular-three-rep0/`

### 20261029-025451-s9_research_count-regular-three-rep1 — s9_research_count × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 8.5 | — | 9.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 8.66 | 0.97 | 4.3692 | 23861 | 544 |

Overall: 5 model requests, latency p50 0.97 s / p95 4.3692 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025451-s9_research_count-regular-three-rep1/`

### 20261029-025456-s9_research_count-regular-three-rep2 — s9_research_count × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 5.4 | — | 5.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 5.506 | 1.2815 | 2.3542 | 18725 | 310 |

Overall: 4 model requests, latency p50 1.2815 s / p95 2.3542 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025456-s9_research_count-regular-three-rep2/`

### 20261029-025507-s9_research_count-regular-three-rep3 — s9_research_count × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 9.9 | — | 10.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 9.728 | 1.01 | 5.0904 | 23971 | 545 |

Overall: 5 model requests, latency p50 1.01 s / p95 5.0904 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025507-s9_research_count-regular-three-rep3/`

### 20261029-025507-s9_research_count-regular-three-rep4 — s9_research_count × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 8.8 | — | 9.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 8.864 | 0.8415 | 5.6785 | 18688 | 261 |

Overall: 4 model requests, latency p50 0.8415 s / p95 5.6785 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025507-s9_research_count-regular-three-rep4/`

### 20261029-025508-s9_research_count-regular-three-rep5 — s9_research_count × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 10.5 | — | 10.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 10.582 | 0.889 | 6.1092 | 23439 | 370 |

Overall: 5 model requests, latency p50 0.889 s / p95 6.1092 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025508-s9_research_count-regular-three-rep5/`

### 20261029-025521-s9_research_count-regular-three-rep6 — s9_research_count × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 3.4 | — | 3.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 3.479 | 0.8505 | 0.9929 | 19007 | 503 |

Overall: 4 model requests, latency p50 0.8505 s / p95 0.9929 s.
Recorder ↔ transcript cross-check: 4/4 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025521-s9_research_count-regular-three-rep6/`

### 20261029-025523-s9_research_count-regular-three-rep7 — s9_research_count × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 4.8 | — | 5.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.331 | 0.755 | 1.327 | 23886 | 440 |

Overall: 5 model requests, latency p50 0.755 s / p95 1.327 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025523-s9_research_count-regular-three-rep7/`

### 20261029-025524-s9_research_count-regular-three-rep8 — s9_research_count × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 4.6 | — | 5.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 4.716 | 0.8125 | 0.9892 | 28446 | 481 |

Overall: 6 model requests, latency p50 0.8125 s / p95 0.9892 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025524-s9_research_count-regular-three-rep8/`

### 20261029-025531-s9_research_count-regular-three-rep9 — s9_research_count × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Посчитайте выручку по data/orders.csv и запишите результат в docs/report.md | research | completed | — | 3.8 | — | 4.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 3.523 | 0.717 | 0.8386 | 23583 | 390 |

Overall: 5 model requests, latency p50 0.717 s / p95 0.8386 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261029-025531-s9_research_count-regular-three-rep9/`

### 20261028-225813-s10_research_facts-deepseek-v4-baseline-rep0 — s10_research_facts × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 48.5 | — | 51.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 50.35 | 8.251 | 14.813 | 36781 | 1914 |

Overall: 6 model requests, latency p50 8.251 s / p95 14.813 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225813-s10_research_facts-deepseek-v4-baseline-rep0/`

### 20261028-225817-s10_research_facts-deepseek-v4-baseline-rep1 — s10_research_facts × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 54.7 | — | 57.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 56.334 | 8.5985 | 18.193 | 36234 | 2221 |

Overall: 6 model requests, latency p50 8.5985 s / p95 18.193 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225817-s10_research_facts-deepseek-v4-baseline-rep1/`

### 20261028-225826-s10_research_facts-deepseek-v4-baseline-rep2 — s10_research_facts × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 47.8 | — | 55.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 54.563 | 8.7795 | 19.864 | 36543 | 2235 |

Overall: 6 model requests, latency p50 8.7795 s / p95 19.864 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225826-s10_research_facts-deepseek-v4-baseline-rep2/`

### 20261028-225909-s10_research_facts-deepseek-v4-baseline-rep3 — s10_research_facts × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 44.4 | — | 51.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 51.088 | 6.525 | 15.792 | 34939 | 1893 |

Overall: 6 model requests, latency p50 6.525 s / p95 15.792 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225909-s10_research_facts-deepseek-v4-baseline-rep3/`

### 20261028-225919-s10_research_facts-deepseek-v4-baseline-rep4 — s10_research_facts × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 45.9 | — | 53.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 53.176 | 8.612 | 12.711 | 42347 | 2220 |

Overall: 7 model requests, latency p50 8.612 s / p95 12.711 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225919-s10_research_facts-deepseek-v4-baseline-rep4/`

### 20261028-225931-s10_research_facts-deepseek-v4-baseline-rep5 — s10_research_facts × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 52.6 | — | 61.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 60.292 | 5.42 | 14.7659 | 52639 | 2091 |

Overall: 8 model requests, latency p50 5.42 s / p95 14.7659 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225931-s10_research_facts-deepseek-v4-baseline-rep5/`

### 20261028-230006-s10_research_facts-deepseek-v4-baseline-rep6 — s10_research_facts × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 50.8 | — | 59.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 58.962 | 9.209 | 21.0428 | 38238 | 2321 |

Overall: 6 model requests, latency p50 9.209 s / p95 21.0428 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230006-s10_research_facts-deepseek-v4-baseline-rep6/`

### 20261028-230017-s10_research_facts-deepseek-v4-baseline-rep7 — s10_research_facts × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 48.9 | — | 56.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 55.636 | 5.446 | 17.508 | 40702 | 1919 |

Overall: 7 model requests, latency p50 5.446 s / p95 17.508 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230017-s10_research_facts-deepseek-v4-baseline-rep7/`

### 20261028-230043-s10_research_facts-deepseek-v4-baseline-rep8 — s10_research_facts × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 51.9 | — | 58.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 57.732 | 6.679 | 16.798 | 42064 | 2031 |

Overall: 7 model requests, latency p50 6.679 s / p95 16.798 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230043-s10_research_facts-deepseek-v4-baseline-rep8/`

### 20261028-230112-s10_research_facts-deepseek-v4-baseline-rep9 — s10_research_facts × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 37.7 | — | 44.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 43.825 | 7.409 | 14.43 | 35088 | 1641 |

Overall: 6 model requests, latency p50 7.409 s / p95 14.43 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230112-s10_research_facts-deepseek-v4-baseline-rep9/`

### 20261028-225725-s10_research_facts-glm-5.3-baseline-rep0 — s10_research_facts × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 12.3 | — | 13.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 12.483 | 1.458 | 3.7387 | 38308 | 1578 |

Overall: 7 model requests, latency p50 1.458 s / p95 3.7387 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225725-s10_research_facts-glm-5.3-baseline-rep0/`

### 20261028-225725-s10_research_facts-glm-5.3-baseline-rep1 — s10_research_facts × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 7.4 | — | 8.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 7.77 | 1.0085 | 2.2128 | 32362 | 1057 |

Overall: 6 model requests, latency p50 1.0085 s / p95 2.2128 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225725-s10_research_facts-glm-5.3-baseline-rep1/`

### 20261028-225725-s10_research_facts-glm-5.3-baseline-rep2 — s10_research_facts × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 11.1 | — | 12 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 11.095 | 1.223 | 2.9786 | 37914 | 1194 |

Overall: 7 model requests, latency p50 1.223 s / p95 2.9786 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225725-s10_research_facts-glm-5.3-baseline-rep2/`

### 20261028-225741-s10_research_facts-glm-5.3-baseline-rep3 — s10_research_facts × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 8.6 | — | 9.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 9.024 | 0.9 | 2.565 | 37450 | 1153 |

Overall: 7 model requests, latency p50 0.9 s / p95 2.565 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225741-s10_research_facts-glm-5.3-baseline-rep3/`

### 20261028-225745-s10_research_facts-glm-5.3-baseline-rep4 — s10_research_facts × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 7.6 | — | 8.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 8.07 | 1.2455 | 2.1498 | 32759 | 1342 |

Overall: 6 model requests, latency p50 1.2455 s / p95 2.1498 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225745-s10_research_facts-glm-5.3-baseline-rep4/`

### 20261028-225746-s10_research_facts-glm-5.3-baseline-rep5 — s10_research_facts × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 7.8 | — | 8.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 8.277 | 1.044 | 2.2207 | 37820 | 1368 |

Overall: 7 model requests, latency p50 1.044 s / p95 2.2207 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225746-s10_research_facts-glm-5.3-baseline-rep5/`

### 20261028-225756-s10_research_facts-glm-5.3-baseline-rep6 — s10_research_facts × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 8 | — | 9.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 8.442 | 0.87 | 2.7665 | 37629 | 1313 |

Overall: 7 model requests, latency p50 0.87 s / p95 2.7665 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225756-s10_research_facts-glm-5.3-baseline-rep6/`

### 20261028-225759-s10_research_facts-glm-5.3-baseline-rep7 — s10_research_facts × glm-5.3-baseline

Reason: `settled but checks.py failed:
S10 checks FAILED:
- git log -- docs/findings.md is empty — the findings were not committed by git_commit_docs (the documentation assignment must end with the agent committing its own changes)`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 7.8 | — | 9.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 8.792 | 1.68 | 3.036 | 26709 | 1441 |

Overall: 5 model requests, latency p50 1.68 s / p95 3.036 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225759-s10_research_facts-glm-5.3-baseline-rep7/`

### 20261028-225800-s10_research_facts-glm-5.3-baseline-rep8 — s10_research_facts × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 10.4 | — | 11.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 10.78 | 1.331 | 2.8478 | 37813 | 1444 |

Overall: 7 model requests, latency p50 1.331 s / p95 2.8478 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225800-s10_research_facts-glm-5.3-baseline-rep8/`

### 20261028-225810-s10_research_facts-glm-5.3-baseline-rep9 — s10_research_facts × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 8.8 | — | 10 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 9.186 | 0.883 | 2.4319 | 45043 | 1565 |

Overall: 7 model requests, latency p50 0.883 s / p95 2.4319 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-225810-s10_research_facts-glm-5.3-baseline-rep9/`

### 20261028-230119-s10_research_facts-incredible-four-rep0 — s10_research_facts × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 51.2 | — | 58.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 57.834 | 9.047 | 15.273 | 39724 | 2131 |

Overall: 6 model requests, latency p50 9.047 s / p95 15.273 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230119-s10_research_facts-incredible-four-rep0/`

### 20261028-230152-s10_research_facts-incredible-four-rep1 — s10_research_facts × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 31.6 | — | 40.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 39.874 | 4.137 | 12.4397 | 39334 | 1583 |

Overall: 7 model requests, latency p50 4.137 s / p95 12.4397 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230152-s10_research_facts-incredible-four-rep1/`

### 20261028-230202-s10_research_facts-incredible-four-rep2 — s10_research_facts × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 42.2 | — | 48.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 48.075 | 4.965 | 12.9504 | 45080 | 1739 |

Overall: 7 model requests, latency p50 4.965 s / p95 12.9504 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230202-s10_research_facts-incredible-four-rep2/`

### 20261028-230223-s10_research_facts-incredible-four-rep3 — s10_research_facts × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 42.3 | — | 49.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 48.409 | 7.523 | 15.5265 | 35953 | 1971 |

Overall: 6 model requests, latency p50 7.523 s / p95 15.5265 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230223-s10_research_facts-incredible-four-rep3/`

### 20261028-230243-s10_research_facts-incredible-four-rep4 — s10_research_facts × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 43.1 | — | 48.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 47.864 | 7.4205 | 15.191 | 35618 | 1882 |

Overall: 6 model requests, latency p50 7.4205 s / p95 15.191 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230243-s10_research_facts-incredible-four-rep4/`

### 20261028-230255-s10_research_facts-incredible-four-rep5 — s10_research_facts × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 38.3 | — | 46.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 45.35 | 7.767 | 14.5128 | 35723 | 1813 |

Overall: 6 model requests, latency p50 7.767 s / p95 14.5128 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230255-s10_research_facts-incredible-four-rep5/`

### 20261028-230317-s10_research_facts-incredible-four-rep6 — s10_research_facts × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 43.6 | — | 53.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 52.706 | 9.484 | 15.575 | 35594 | 2032 |

Overall: 6 model requests, latency p50 9.484 s / p95 15.575 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230317-s10_research_facts-incredible-four-rep6/`

### 20261028-230337-s10_research_facts-incredible-four-rep7 — s10_research_facts × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 38.3 | — | 44.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 43.712 | 5.462 | 13.0035 | 41910 | 1821 |

Overall: 7 model requests, latency p50 5.462 s / p95 13.0035 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230337-s10_research_facts-incredible-four-rep7/`

### 20261028-230351-s10_research_facts-incredible-four-rep8 — s10_research_facts × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 36.5 | — | 43.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 42.591 | 7.4165 | 13.3028 | 35346 | 1914 |

Overall: 6 model requests, latency p50 7.4165 s / p95 13.3028 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230351-s10_research_facts-incredible-four-rep8/`

### 20261028-230416-s10_research_facts-incredible-four-rep9 — s10_research_facts × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 34.5 | — | 40.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 39.371 | 4.792 | 12.511 | 40683 | 1657 |

Overall: 7 model requests, latency p50 4.792 s / p95 12.511 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230416-s10_research_facts-incredible-four-rep9/`

### 20261028-230427-s10_research_facts-regular-three-rep0 — s10_research_facts × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 8.5 | — | 9.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 9.24 | 0.7365 | 2.6463 | 42818 | 1463 |

Overall: 8 model requests, latency p50 0.7365 s / p95 2.6463 s.
Recorder ↔ transcript cross-check: 8/8 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230427-s10_research_facts-regular-three-rep0/`

### 20261028-230439-s10_research_facts-regular-three-rep1 — s10_research_facts × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 7.9 | — | 8.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 8.189 | 0.848 | 2.4602 | 37713 | 1278 |

Overall: 7 model requests, latency p50 0.848 s / p95 2.4602 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230439-s10_research_facts-regular-three-rep1/`

### 20261028-230441-s10_research_facts-regular-three-rep2 — s10_research_facts × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 14 | — | 16.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 15.359 | 1.952 | 4.5416 | 37919 | 1395 |

Overall: 7 model requests, latency p50 1.952 s / p95 4.5416 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230441-s10_research_facts-regular-three-rep2/`

### 20261028-230453-s10_research_facts-regular-three-rep3 — s10_research_facts × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 7.7 | — | 8.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 8.177 | 0.783 | 2.5327 | 38109 | 1291 |

Overall: 7 model requests, latency p50 0.783 s / p95 2.5327 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230453-s10_research_facts-regular-three-rep3/`

### 20261028-230502-s10_research_facts-regular-three-rep4 — s10_research_facts × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 8.4 | — | 9.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 9.031 | 1.1495 | 2.6515 | 33264 | 1437 |

Overall: 6 model requests, latency p50 1.1495 s / p95 2.6515 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230502-s10_research_facts-regular-three-rep4/`

### 20261028-230506-s10_research_facts-regular-three-rep5 — s10_research_facts × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 9.2 | — | 10.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 10.018 | 1.55 | 2.899 | 32718 | 1295 |

Overall: 6 model requests, latency p50 1.55 s / p95 2.899 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230506-s10_research_facts-regular-three-rep5/`

### 20261028-230506-s10_research_facts-regular-three-rep6 — s10_research_facts × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 7.6 | — | 9.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 8.668 | 1.2 | 2.4402 | 32822 | 1242 |

Overall: 6 model requests, latency p50 1.2 s / p95 2.4402 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230506-s10_research_facts-regular-three-rep6/`

### 20261028-230517-s10_research_facts-regular-three-rep7 — s10_research_facts × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 10.4 | — | 11.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 10.855 | 1.273 | 3.0013 | 38316 | 1502 |

Overall: 7 model requests, latency p50 1.273 s / p95 3.0013 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230517-s10_research_facts-regular-three-rep7/`

### 20261028-230521-s10_research_facts-regular-three-rep8 — s10_research_facts × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 8.9 | — | 10.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 9.917 | 1.096 | 2.4368 | 38187 | 1518 |

Overall: 7 model requests, latency p50 1.096 s / p95 2.4368 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230521-s10_research_facts-regular-three-rep8/`

### 20261028-230522-s10_research_facts-regular-three-rep9 — s10_research_facts × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Найдите в кодовой базе три факта и опишите их в docs/findings.md | research | completed | — | 10 | — | 11.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 10.716 | 0.973 | 3.4697 | 38232 | 1447 |

Overall: 7 model requests, latency p50 0.973 s / p95 3.4697 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230522-s10_research_facts-regular-three-rep9/`

### 20261028-230620-s11_research_routes-deepseek-v4-baseline-rep0 — s11_research_routes × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 18.7 | — | 27.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 26.781 | 2.863 | 8.2 | 36670 | 894 |

Overall: 7 model requests, latency p50 2.863 s / p95 8.2 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230620-s11_research_routes-deepseek-v4-baseline-rep0/`

### 20261028-230622-s11_research_routes-deepseek-v4-baseline-rep1 — s11_research_routes × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 15.6 | — | 20.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 19.415 | 3.0765 | 5.0202 | 31500 | 720 |

Overall: 6 model requests, latency p50 3.0765 s / p95 5.0202 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230622-s11_research_routes-deepseek-v4-baseline-rep1/`

### 20261028-230623-s11_research_routes-deepseek-v4-baseline-rep2 — s11_research_routes × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 24.1 | — | 29.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 28.671 | 2.722 | 8.4408 | 37817 | 909 |

Overall: 7 model requests, latency p50 2.722 s / p95 8.4408 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230623-s11_research_routes-deepseek-v4-baseline-rep2/`

### 20261028-230648-s11_research_routes-deepseek-v4-baseline-rep3 — s11_research_routes × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 19.2 | — | 24.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 23.958 | 3.118 | 5.723 | 37883 | 861 |

Overall: 7 model requests, latency p50 3.118 s / p95 5.723 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230648-s11_research_routes-deepseek-v4-baseline-rep3/`

### 20261028-230655-s11_research_routes-deepseek-v4-baseline-rep4 — s11_research_routes × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 17.2 | — | 21.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 21.127 | 3.1295 | 5.3592 | 31818 | 825 |

Overall: 6 model requests, latency p50 3.1295 s / p95 5.3592 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230655-s11_research_routes-deepseek-v4-baseline-rep4/`

### 20261028-230704-s11_research_routes-deepseek-v4-baseline-rep5 — s11_research_routes × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 13.7 | — | 19.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 18.868 | 3.401 | 6.2036 | 25617 | 772 |

Overall: 5 model requests, latency p50 3.401 s / p95 6.2036 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230704-s11_research_routes-deepseek-v4-baseline-rep5/`

### 20261028-230718-s11_research_routes-deepseek-v4-baseline-rep6 — s11_research_routes × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 13 | — | 17.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 16.859 | 3.001 | 5.0584 | 25588 | 667 |

Overall: 5 model requests, latency p50 3.001 s / p95 5.0584 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230718-s11_research_routes-deepseek-v4-baseline-rep6/`

### 20261028-230722-s11_research_routes-deepseek-v4-baseline-rep7 — s11_research_routes × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 18.3 | — | 24.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 23.547 | 3.729 | 6.1542 | 31792 | 891 |

Overall: 6 model requests, latency p50 3.729 s / p95 6.1542 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230722-s11_research_routes-deepseek-v4-baseline-rep7/`

### 20261028-230729-s11_research_routes-deepseek-v4-baseline-rep8 — s11_research_routes × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 17 | — | 22.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 21.503 | 3.403 | 5.8742 | 31090 | 750 |

Overall: 6 model requests, latency p50 3.403 s / p95 5.8742 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230729-s11_research_routes-deepseek-v4-baseline-rep8/`

### 20261028-230741-s11_research_routes-deepseek-v4-baseline-rep9 — s11_research_routes × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 14.6 | — | 18.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 18.288 | 3.246 | 5.5022 | 25776 | 769 |

Overall: 5 model requests, latency p50 3.246 s / p95 5.5022 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230741-s11_research_routes-deepseek-v4-baseline-rep9/`

### 20261028-230535-s11_research_routes-glm-5.3-baseline-rep0 — s11_research_routes × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 9.3 | — | 9.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 8.968 | 1.108 | 4.4244 | 25711 | 473 |

Overall: 5 model requests, latency p50 1.108 s / p95 4.4244 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230535-s11_research_routes-glm-5.3-baseline-rep0/`

### 20261028-230542-s11_research_routes-glm-5.3-baseline-rep1 — s11_research_routes × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 9.5 | — | 10.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 9.386 | 0.951 | 4.6112 | 24539 | 434 |

Overall: 5 model requests, latency p50 0.951 s / p95 4.6112 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230542-s11_research_routes-glm-5.3-baseline-rep1/`

### 20261028-230543-s11_research_routes-glm-5.3-baseline-rep2 — s11_research_routes × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 10.2 | — | 11 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 10.156 | 0.788 | 5.9618 | 24422 | 343 |

Overall: 5 model requests, latency p50 0.788 s / p95 5.9618 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230543-s11_research_routes-glm-5.3-baseline-rep2/`

### 20261028-230550-s11_research_routes-glm-5.3-baseline-rep3 — s11_research_routes × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 4.9 | — | 5.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.793 | 0.82 | 1.432 | 24574 | 420 |

Overall: 5 model requests, latency p50 0.82 s / p95 1.432 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230550-s11_research_routes-glm-5.3-baseline-rep3/`

### 20261028-230557-s11_research_routes-glm-5.3-baseline-rep4 — s11_research_routes × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 4.1 | — | 5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.3 | 0.809 | 1.3444 | 24460 | 418 |

Overall: 5 model requests, latency p50 0.809 s / p95 1.3444 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230557-s11_research_routes-glm-5.3-baseline-rep4/`

### 20261028-230600-s11_research_routes-glm-5.3-baseline-rep5 — s11_research_routes × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 4.5 | — | 8.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 7.34 | 0.746 | 3.7498 | 24606 | 387 |

Overall: 5 model requests, latency p50 0.746 s / p95 3.7498 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230600-s11_research_routes-glm-5.3-baseline-rep5/`

### 20261028-230601-s11_research_routes-glm-5.3-baseline-rep6 — s11_research_routes × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 4.5 | — | 5.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 4.435 | 0.5645 | 1.221 | 30186 | 414 |

Overall: 6 model requests, latency p50 0.5645 s / p95 1.221 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230601-s11_research_routes-glm-5.3-baseline-rep6/`

### 20261028-230608-s11_research_routes-glm-5.3-baseline-rep7 — s11_research_routes × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 5.2 | — | 6.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 5.548 | 1.134 | 1.5138 | 25068 | 440 |

Overall: 5 model requests, latency p50 1.134 s / p95 1.5138 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230608-s11_research_routes-glm-5.3-baseline-rep7/`

### 20261028-230611-s11_research_routes-glm-5.3-baseline-rep8 — s11_research_routes × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 3.8 | — | 4.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 3.651 | 0.743 | 0.9728 | 24547 | 393 |

Overall: 5 model requests, latency p50 0.743 s / p95 0.9728 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230611-s11_research_routes-glm-5.3-baseline-rep8/`

### 20261028-230613-s11_research_routes-glm-5.3-baseline-rep9 — s11_research_routes × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 4.5 | — | 5.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.442 | 0.964 | 1.0868 | 25334 | 497 |

Overall: 5 model requests, latency p50 0.964 s / p95 1.0868 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230613-s11_research_routes-glm-5.3-baseline-rep9/`

### 20261028-230753-s11_research_routes-incredible-four-rep0 — s11_research_routes × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 11.6 | — | 17.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 16.752 | 2.612 | 6.0552 | 25674 | 665 |

Overall: 5 model requests, latency p50 2.612 s / p95 6.0552 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230753-s11_research_routes-incredible-four-rep0/`

### 20261028-230801-s11_research_routes-incredible-four-rep1 — s11_research_routes × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 16.4 | — | 20.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 19.871 | 3.384 | 4.5198 | 31108 | 663 |

Overall: 6 model requests, latency p50 3.384 s / p95 4.5198 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230801-s11_research_routes-incredible-four-rep1/`

### 20261028-230804-s11_research_routes-incredible-four-rep2 — s11_research_routes × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 20.3 | — | 25.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 24.672 | 3.5305 | 6.6482 | 32619 | 909 |

Overall: 6 model requests, latency p50 3.5305 s / p95 6.6482 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230804-s11_research_routes-incredible-four-rep2/`

### 20261028-230815-s11_research_routes-incredible-four-rep3 — s11_research_routes × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 12.7 | — | 17.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 16.608 | 3.444 | 4.8452 | 25645 | 674 |

Overall: 5 model requests, latency p50 3.444 s / p95 4.8452 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230815-s11_research_routes-incredible-four-rep3/`

### 20261028-230828-s11_research_routes-incredible-four-rep4 — s11_research_routes × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 26.6 | — | 31.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 18.688 | 3.919 | 5.778 | 25576 | 690 |

Overall: 5 model requests, latency p50 3.919 s / p95 5.778 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230828-s11_research_routes-incredible-four-rep4/`

### 20261028-230834-s11_research_routes-incredible-four-rep5 — s11_research_routes × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 20.6 | — | 25.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 21.521 | 3.35 | 6.1202 | 31885 | 799 |

Overall: 6 model requests, latency p50 3.35 s / p95 6.1202 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230834-s11_research_routes-incredible-four-rep5/`

### 20261028-230837-s11_research_routes-incredible-four-rep6 — s11_research_routes × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 20.6 | — | 25.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 24.616 | 3.134 | 6.0723 | 37964 | 841 |

Overall: 7 model requests, latency p50 3.134 s / p95 6.0723 s.
Recorder ↔ transcript cross-check: 7/7 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230837-s11_research_routes-incredible-four-rep6/`

### 20261028-230906-s11_research_routes-incredible-four-rep7 — s11_research_routes × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 17.8 | — | 24.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 23.587 | 3.7395 | 6.4635 | 31851 | 846 |

Overall: 6 model requests, latency p50 3.7395 s / p95 6.4635 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230906-s11_research_routes-incredible-four-rep7/`

### 20261028-230908-s11_research_routes-incredible-four-rep8 — s11_research_routes × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 18.8 | — | 25.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 25.16 | 3.806 | 7.845 | 31842 | 877 |

Overall: 6 model requests, latency p50 3.806 s / p95 7.845 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230908-s11_research_routes-incredible-four-rep8/`

### 20261028-230909-s11_research_routes-incredible-four-rep9 — s11_research_routes × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 19.4 | — | 24.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 24.204 | 3.8825 | 7.1762 | 31749 | 812 |

Overall: 6 model requests, latency p50 3.8825 s / p95 7.1762 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230909-s11_research_routes-incredible-four-rep9/`

### 20261028-230936-s11_research_routes-regular-three-rep0 — s11_research_routes × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 5.8 | — | 6.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 5.555 | 1.109 | 1.4846 | 25220 | 434 |

Overall: 5 model requests, latency p50 1.109 s / p95 1.4846 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230936-s11_research_routes-regular-three-rep0/`

### 20261028-230939-s11_research_routes-regular-three-rep1 — s11_research_routes × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 5.4 | — | 6.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 5.316 | 1.107 | 1.3622 | 24481 | 359 |

Overall: 5 model requests, latency p50 1.107 s / p95 1.3622 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230939-s11_research_routes-regular-three-rep1/`

### 20261028-230940-s11_research_routes-regular-three-rep2 — s11_research_routes × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 6.4 | — | 7.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 6.657 | 1.1255 | 1.4288 | 30338 | 489 |

Overall: 6 model requests, latency p50 1.1255 s / p95 1.4288 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230940-s11_research_routes-regular-three-rep2/`

### 20261028-230953-s11_research_routes-regular-three-rep3 — s11_research_routes × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 5.4 | — | 6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 5.329 | 0.996 | 1.5412 | 25456 | 543 |

Overall: 5 model requests, latency p50 0.996 s / p95 1.5412 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230953-s11_research_routes-regular-three-rep3/`

### 20261028-230953-s11_research_routes-regular-three-rep4 — s11_research_routes × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 5.6 | — | 6.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 5.423 | 0.986 | 1.032 | 30472 | 516 |

Overall: 6 model requests, latency p50 0.986 s / p95 1.032 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230953-s11_research_routes-regular-three-rep4/`

### 20261028-230954-s11_research_routes-regular-three-rep5 — s11_research_routes × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 12 | — | 12.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 12.076 | 1.028 | 7.1668 | 24646 | 479 |

Overall: 5 model requests, latency p50 1.028 s / p95 7.1668 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-230954-s11_research_routes-regular-three-rep5/`

### 20261028-231005-s11_research_routes-regular-three-rep6 — s11_research_routes × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 4.8 | — | 5.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.462 | 0.917 | 1.0444 | 24628 | 426 |

Overall: 5 model requests, latency p50 0.917 s / p95 1.0444 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231005-s11_research_routes-regular-three-rep6/`

### 20261028-231005-s11_research_routes-regular-three-rep7 — s11_research_routes × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 4.5 | — | 5.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.305 | 0.974 | 0.9884 | 24892 | 387 |

Overall: 5 model requests, latency p50 0.974 s / p95 0.9884 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231005-s11_research_routes-regular-three-rep7/`

### 20261028-231012-s11_research_routes-regular-three-rep8 — s11_research_routes × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 4.6 | — | 5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.289 | 0.822 | 1.0702 | 25352 | 423 |

Overall: 5 model requests, latency p50 0.822 s / p95 1.0702 s.
Recorder ↔ transcript cross-check: 5/5 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231012-s11_research_routes-regular-three-rep8/`

### 20261028-231015-s11_research_routes-regular-three-rep9 — s11_research_routes × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте полный список маршрутов API в docs/routes.md | research | completed | — | 6.1 | — | 7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 6.252 | 1.0205 | 1.4445 | 30871 | 499 |

Overall: 6 model requests, latency p50 1.0205 s / p95 1.4445 s.
Recorder ↔ transcript cross-check: 6/6 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231015-s11_research_routes-regular-three-rep9/`

### 20261028-231154-s12_research_bug_report-deepseek-v4-baseline-rep0 — s12_research_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 36.2 | — | 45.3 |
| Считать партии отгрузки с округлением вверх в batches_needed | bug | completed | Verified successfully | 16.7 | 30.2 | 50 |

Bug round-trips:

- `a8e464a5` Считать партии отгрузки с округлением вверх в batches_needed (activated 2026-10-28T20:12:43.733483+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 89.694 | 4.376 | 13.2662 | 65723 | 3386 |

Overall: 16 model requests, latency p50 4.376 s / p95 13.2662 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231154-s12_research_bug_report-deepseek-v4-baseline-rep0/`

### 20261028-231213-s12_research_bug_report-deepseek-v4-baseline-rep1 — s12_research_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 32.4 | — | 41.9 |
| batches_needed не учитывает последнюю неполную партию | bug | completed | Verified successfully | 18.3 | 28.8 | 55.2 |

Bug round-trips:

- `b9f7de28` batches_needed не учитывает последнюю неполную партию (activated 2026-10-28T20:12:59.863327+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 15 | 86.629 | 4.329 | 14.4573 | 59827 | 3043 |

Overall: 15 model requests, latency p50 4.329 s / p95 14.4573 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231213-s12_research_bug_report-deepseek-v4-baseline-rep1/`

### 20261028-231216-s12_research_bug_report-deepseek-v4-baseline-rep2 — s12_research_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed returns floor instead of ceiling, violating the partial-batch contract | bug | completed | Verified successfully | 14.2 | 32.7 | 54.5 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 19.8 | — | 27.3 |

Bug round-trips:

- `99d83ce9` batches_needed returns floor instead of ceiling, violating the partial-batch contract (activated 2026-10-28T20:12:48.332537+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 14 | 72.302 | 4.2365 | 9.521 | 55927 | 2631 |

Overall: 14 model requests, latency p50 4.2365 s / p95 9.521 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231216-s12_research_bug_report-deepseek-v4-baseline-rep2/`

### 20261028-231336-s12_research_bug_report-deepseek-v4-baseline-rep3 — s12_research_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 36.1 | — | 44.9 |
| batches_needed не учитывает неполную последнюю партию | bug | completed | Verified successfully | 9.5 | 29 | 47.6 |

Bug round-trips:

- `dca41592` batches_needed не учитывает неполную последнюю партию (activated 2026-10-28T20:14:31.113642+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 80.598 | 3.473 | 10.5022 | 66694 | 3279 |

Overall: 16 model requests, latency p50 3.473 s / p95 10.5022 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231336-s12_research_bug_report-deepseek-v4-baseline-rep3/`

### 20261028-231339-s12_research_bug_report-deepseek-v4-baseline-rep4 — s12_research_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 24.5 | — | 32.7 |
| batches_needed использует целочисленное деление с округлением вниз вместо округления вверх | bug | completed | Verified successfully | 5.2 | 24.6 | 39.9 |

Bug round-trips:

- `f6bc56cb` batches_needed использует целочисленное деление с округлением вниз вместо округления вверх (activated 2026-10-28T20:14:18.976754+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 12 | 61.223 | 3.024 | 14.39 | 47149 | 2459 |

Overall: 12 model requests, latency p50 3.024 s / p95 14.39 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231339-s12_research_bug_report-deepseek-v4-baseline-rep4/`

### 20261028-231350-s12_research_bug_report-deepseek-v4-baseline-rep5 — s12_research_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed не учитывает последнюю неполную партию (занижает число партий) | bug | completed | Verified successfully | 12 | 28.4 | 50.6 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 22.5 | — | 32.7 |

Bug round-trips:

- `843de643` batches_needed не учитывает последнюю неполную партию (занижает число партий) (activated 2026-10-28T20:14:27.632373+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 14 | 68.876 | 4.01 | 10.4938 | 55675 | 2850 |

Overall: 14 model requests, latency p50 4.01 s / p95 10.4938 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231350-s12_research_bug_report-deepseek-v4-baseline-rep5/`

### 20261028-231452-s12_research_bug_report-deepseek-v4-baseline-rep6 — s12_research_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 35.2 | — | 45.4 |
| batches_needed использует деление нацело вместо округления вверх, занижая число партий для неполных партий | bug | completed | Verified successfully | 13.8 | 23.9 | 47.9 |

Bug round-trips:

- `887de3d9` batches_needed использует деление нацело вместо округления вверх, занижая число партий для неполных партий (activated 2026-10-28T20:15:47.918842+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 14 | 79.721 | 3.9495 | 11.75 | 58862 | 3249 |

Overall: 14 model requests, latency p50 3.9495 s / p95 11.75 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231452-s12_research_bug_report-deepseek-v4-baseline-rep6/`

### 20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep7 — s12_research_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed использует деление нацело вместо округления вверх — занижает число партий | bug | completed | Verified successfully | 9.9 | 21.8 | 44 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 27.6 | — | 39.6 |

Bug round-trips:

- `8c05fc96` batches_needed использует деление нацело вместо округления вверх — занижает число партий (activated 2026-10-28T20:15:56.459731+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 13 | 70.801 | 3.649 | 17.3724 | 50949 | 2954 |

Overall: 13 model requests, latency p50 3.649 s / p95 17.3724 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep7/`

### 20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep8 — s12_research_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 25.5 | — | 36.5 |
| batches_needed не учитывает последнюю неполную партию (floor вместо ceiling) | bug | completed | Verified successfully | 8.9 | 26.3 | 46.7 |

Bug round-trips:

- `424a8ee4` batches_needed не учитывает последнюю неполную партию (floor вместо ceiling) (activated 2026-10-28T20:15:53.311425+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 15 | 70.062 | 3.281 | 13.0353 | 60458 | 2837 |

Overall: 15 model requests, latency p50 3.281 s / p95 13.0353 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231512-s12_research_bug_report-deepseek-v4-baseline-rep8/`

### 20261028-231631-s12_research_bug_report-deepseek-v4-baseline-rep9 — s12_research_bug_report × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 25.6 | — | 36.2 |
| pricing.batches_needed округляет вниз и теряет последнюю неполную партию | bug | completed | Verified successfully | 17 | 30.1 | 58.3 |

Bug round-trips:

- `caefd63d` pricing.batches_needed округляет вниз и теряет последнюю неполную партию (activated 2026-10-28T20:17:17.726297+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 84.593 | 3.5055 | 11.07 | 64136 | 3247 |

Overall: 16 model requests, latency p50 3.5055 s / p95 11.07 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231631-s12_research_bug_report-deepseek-v4-baseline-rep9/`

### 20261028-231015-s12_research_bug_report-glm-5.3-baseline-rep0 — s12_research_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed округляет партии вниз — теряется последняя неполная партия | bug | completed | Verified successfully | 4.7 | 6.6 | 12.2 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 5.3 | — | 6.2 |

Bug round-trips:

- `3f206061` batches_needed округляет партии вниз — теряется последняя неполная партия (activated 2026-10-28T20:10:26.239458+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 13.673 | 0.858 | 2.3118 | 48832 | 1955 |

Overall: 13 model requests, latency p50 0.858 s / p95 2.3118 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231015-s12_research_bug_report-glm-5.3-baseline-rep0/`

### 20261028-231023-s12_research_bug_report-glm-5.3-baseline-rep1 — s12_research_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 4.4 | — | 7.9 |
| batches_needed отбрасывает неполную партию вместо округления вверх | bug | completed | Verified successfully | 6.2 | 10.9 | 20.3 |

Bug round-trips:

- `88ef4088` batches_needed отбрасывает неполную партию вместо округления вверх (activated 2026-10-28T20:10:35.158152+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 19.776 | 0.987 | 3.6862 | 49785 | 2036 |

Overall: 13 model requests, latency p50 0.987 s / p95 3.6862 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231023-s12_research_bug_report-glm-5.3-baseline-rep1/`

### 20261028-231027-s12_research_bug_report-glm-5.3-baseline-rep2 — s12_research_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed считает партии целочисленным делением вместо округления вверх | bug | completed | Verified successfully | 4.4 | 7.1 | 13.3 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 5.2 | — | 6.6 |

Bug round-trips:

- `1c57d02e` batches_needed считает партии целочисленным делением вместо округления вверх (activated 2026-10-28T20:10:38.347719+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 13.307 | 0.873 | 2.7476 | 48576 | 1536 |

Overall: 12 model requests, latency p50 0.873 s / p95 2.7476 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231027-s12_research_bug_report-glm-5.3-baseline-rep2/`

### 20261028-231041-s12_research_bug_report-glm-5.3-baseline-rep3 — s12_research_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 4.4 | — | 5.2 |
| batches_needed округляет число партий вниз вместо округления вверх | bug | completed | Verified successfully | 6.8 | 9.1 | 35.5 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:batches_needed округляет число партий вниз вместо округления вверх', 'tester': 'bug:batches_needed округляет число партий вниз вместо округления вверх round 0', 'at': '2026-10-28T20:11:11.801478+00:00', 'detail': 'coder message at 2026-10-28T20:11:11.801478+00:00 inside tester interval 2026-10-28T20:11:04.266507+00:00…2026-10-28T20:11:12.254141+00:00'}

Bug round-trips:

- `79ea3e7e` batches_needed округляет число партий вниз вместо округления вверх (activated 2026-10-28T20:11:13.556938+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 22 | 33.536 | 1.255 | 2.5651 | 89060 | 3992 |

Overall: 22 model requests, latency p50 1.255 s / p95 2.5651 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231041-s12_research_bug_report-glm-5.3-baseline-rep3/`

### 20261028-231052-s12_research_bug_report-glm-5.3-baseline-rep4 — s12_research_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 9.3 | — | 11 |
| Исправить batches_needed в dispatch/pricing.py: floor вместо округления вверх | bug | completed | Verified successfully | 4.4 | 6.4 | 12.6 |

Bug round-trips:

- `60201e63` Исправить batches_needed в dispatch/pricing.py: floor вместо округления вверх (activated 2026-10-28T20:11:08.037642+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 18.303 | 0.88 | 4.1902 | 49530 | 1785 |

Overall: 12 model requests, latency p50 0.88 s / p95 4.1902 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231052-s12_research_bug_report-glm-5.3-baseline-rep4/`

### 20261028-231054-s12_research_bug_report-glm-5.3-baseline-rep5 — s12_research_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed не учитывает последнюю неполную партию (округление вниз вместо вверх) | bug | completed | Verified successfully | 4.5 | 11.3 | 16.9 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 8.4 | — | 9.4 |

Bug round-trips:

- `06b3c30b` batches_needed не учитывает последнюю неполную партию (округление вниз вместо вверх) (activated 2026-10-28T20:11:07.741649+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 22.367 | 1.2755 | 3.7778 | 61870 | 2601 |

Overall: 14 model requests, latency p50 1.2755 s / p95 3.7778 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231054-s12_research_bug_report-glm-5.3-baseline-rep5/`

### 20261028-231122-s12_research_bug_report-glm-5.3-baseline-rep6 — s12_research_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 4.6 | — | 5.7 |
| batches_needed не учитывает последнюю неполную партию (нет округления вверх) | bug | completed | Verified successfully | 4 | 6.1 | 11.7 |

Bug round-trips:

- `fd8cb43c` batches_needed не учитывает последнюю неполную партию (нет округления вверх) (activated 2026-10-28T20:11:32.290469+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 12.916 | 0.728 | 2.0964 | 54758 | 1562 |

Overall: 13 model requests, latency p50 0.728 s / p95 2.0964 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231122-s12_research_bug_report-glm-5.3-baseline-rep6/`

### 20261028-231127-s12_research_bug_report-glm-5.3-baseline-rep7 — s12_research_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed округляет вниз вместо округления вверх — неполная последняя партия теряется | bug | completed | Verified successfully | 4.9 | 8.6 | 15 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 5.4 | — | 6.8 |

Bug round-trips:

- `29813252` batches_needed округляет вниз вместо округления вверх — неполная последняя партия теряется (activated 2026-10-28T20:11:37.999432+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 16.009 | 1.041 | 2.7308 | 55572 | 2009 |

Overall: 13 model requests, latency p50 1.041 s / p95 2.7308 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231127-s12_research_bug_report-glm-5.3-baseline-rep7/`

### 20261028-231132-s12_research_bug_report-glm-5.3-baseline-rep8 — s12_research_bug_report × glm-5.3-baseline

Reason: `settled but checks.py failed:
S12 checks FAILED:
- expected exactly 1 non-brief task with kind=bug (the research agent's create_bug_report product), found 2
- bug task bbaf67a6: description does not name the defect's code identifiers — 'dispatch/pricing.py' missing; the report must cite the file path AND the function name verbatim
- bug task bbaf67a6: description does not name the defect's code identifiers — 'batches_needed' missing; the report must cite the file path AND the function name verbatim
- research transcript: create_bug_report called 2 times, expected exactly 1 (the brief authorizes ONE report for the ONE latent defect)`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 9 | — | 10.2 |
| is_tracking_code принимает не-ASCII «цифры» как валидные | bug | completed | Verified successfully | 4.7 | 7.8 | 13.9 |
| batches_needed округляет число партий вниз вместо округления вверх | bug | completed | Verified successfully | 4.3 | 6.8 | 25.5 |

Bug round-trips:

- `bbaf67a6` is_tracking_code принимает не-ASCII «цифры» как валидные (activated 2026-10-28T20:11:46.635973+00:00)
- `e53a64bb` batches_needed округляет число партий вниз вместо округления вверх (activated 2026-10-28T20:11:59.707200+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 27 | 28.215 | 0.802 | 2.5988 | 99644 | 3559 |

Overall: 27 model requests, latency p50 0.802 s / p95 2.5988 s.
Recorder ↔ transcript cross-check: 27/27 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231132-s12_research_bug_report-glm-5.3-baseline-rep8/`

### 20261028-231144-s12_research_bug_report-glm-5.3-baseline-rep9 — s12_research_bug_report × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 7.7 | — | 8.9 |
| batches_needed округляет вниз вместо вверх: теряется неполная партия | bug | completed | Verified successfully | 3.7 | 7.5 | 12.4 |

Bug round-trips:

- `e445d72e` batches_needed округляет вниз вместо вверх: теряется неполная партия (activated 2026-10-28T20:12:02.262912+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 17.406 | 0.798 | 3.277 | 53605 | 1949 |

Overall: 14 model requests, latency p50 0.798 s / p95 3.277 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231144-s12_research_bug_report-glm-5.3-baseline-rep9/`

### 20261028-231631-s12_research_bug_report-incredible-four-rep0 — s12_research_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 19.7 | — | 27.5 |
| batches_needed возвращает неверное число партий при неполной последней партии | bug | completed | Verified successfully | 6.4 | 17.8 | 32.7 |

Bug round-trips:

- `f54bb4f5` batches_needed возвращает неверное число партий при неполной последней партии (activated 2026-10-28T20:17:09.084984+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 3 | 27.233 | 9.109 | 14.6152 | 15615 | 1130 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.569 | 0.6605 | 0.7343 | 10097 | 245 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 15.357 | 1.705 | 5.2105 | 36056 | 1845 |

Overall: 13 model requests, latency p50 1.625 s / p95 11.5562 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231631-s12_research_bug_report-incredible-four-rep0/`

### 20261028-231633-s12_research_bug_report-incredible-four-rep1 — s12_research_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed не учитывает последнюю неполную партию (floor division вместо округления вверх) | bug | completed | Verified successfully | 4.3 | 16.8 | 34.7 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 30.6 | — | 44 |

Bug round-trips:

- `0bd7eda2` batches_needed не учитывает последнюю неполную партию (floor division вместо округления вверх) (activated 2026-10-28T20:17:25.580290+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 43.62 | 8.952 | 13.3204 | 27565 | 1714 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 3.683 | 0.667 | 1.123 | 14829 | 443 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 12.791 | 1.799 | 2.4888 | 40765 | 2109 |

Overall: 17 model requests, latency p50 1.799 s / p95 10.8196 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231633-s12_research_bug_report-incredible-four-rep1/`

### 20261028-231737-s12_research_bug_report-incredible-four-rep2 — s12_research_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 30.9 | — | 40.2 |
| batches_needed занижает число партий при неполной последней партии | bug | completed | Verified successfully | 5.6 | 15.1 | 30 |

Bug round-trips:

- `da4b091c` batches_needed занижает число партий при неполной последней партии (activated 2026-10-28T20:18:26.528549+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 39.901 | 8.7445 | 17.3632 | 22298 | 1703 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 3.086 | 0.6785 | 1.029 | 11334 | 373 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 13.424 | 1.9895 | 3.6865 | 29981 | 2311 |

Overall: 14 model requests, latency p50 1.9895 s / p95 12.9772 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231737-s12_research_bug_report-incredible-four-rep2/`

### 20261028-231749-s12_research_bug_report-incredible-four-rep3 — s12_research_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed игнорирует неполную последнюю партию (floor вместо ceil) | bug | completed | Verified successfully | 3.7 | 15.2 | 27.8 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 42.9 | — | 51.4 |

Bug round-trips:

- `b718c988` batches_needed игнорирует неполную последнюю партию (floor вместо ceil) (activated 2026-10-28T20:18:44.936845+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 51.17 | 6.516 | 22.7978 | 27796 | 2070 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.91 | 0.704 | 0.9249 | 11235 | 246 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 13.87 | 1.517 | 4.3028 | 34686 | 1899 |

Overall: 16 model requests, latency p50 1.5955 s / p95 13.6122 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231749-s12_research_bug_report-incredible-four-rep3/`

### 20261028-231812-s12_research_bug_report-incredible-four-rep4 — s12_research_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed возвращает неверное число партий при неполной последней партии | bug | completed | Verified successfully | 3.6 | 17 | 30.6 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 23.5 | — | 33.4 |

Bug round-trips:

- `1c677a25` batches_needed возвращает неверное число партий при неполной последней партии (activated 2026-10-28T20:18:49.861943+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 3 | 33.174 | 10.738 | 18.856 | 15822 | 1432 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 2.835 | 0.61 | 1.0423 | 10461 | 303 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 9 | 15.593 | 1.345 | 3.672 | 44165 | 1845 |

Overall: 16 model requests, latency p50 1.3265 s / p95 12.993 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231812-s12_research_bug_report-incredible-four-rep4/`

### 20261028-231850-s12_research_bug_report-incredible-four-rep5 — s12_research_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 40.7 | — | 51.1 |
| batches_needed не учитывает последнюю неполную партию (ceil вместо floor) | bug | completed | Verified successfully | 5.8 | 20.9 | 37 |

Bug round-trips:

- `bb1cdcf5` batches_needed не учитывает последнюю неполную партию (ceil вместо floor) (activated 2026-10-28T20:19:49.016052+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 50.72 | 10.987 | 13.1888 | 27788 | 1813 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 4.042 | 0.7325 | 1.7153 | 11304 | 305 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 19.927 | 2.0105 | 4.7782 | 55810 | 3036 |

Overall: 17 model requests, latency p50 2.17 s / p95 13.0322 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231850-s12_research_bug_report-incredible-four-rep5/`

### 20261028-231908-s12_research_bug_report-incredible-four-rep6 — s12_research_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 28 | — | 41.2 |
| batches_needed не учитывает неполную последнюю партию (возвращает остаток вместо округления вверх) | bug | completed | Verified successfully | 4.2 | 11.1 | 28.9 |

Bug round-trips:

- `df043942` batches_needed не учитывает неполную последнюю партию (возвращает остаток вместо округления вверх) (activated 2026-10-28T20:19:53.315323+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 40.848 | 9.02 | 13.1894 | 27221 | 1471 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 3.605 | 0.9305 | 1.0286 | 10342 | 339 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 9.435 | 1.5795 | 1.8728 | 36496 | 1514 |

Overall: 15 model requests, latency p50 1.605 s / p95 11.2154 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231908-s12_research_bug_report-incredible-four-rep6/`

### 20261028-231913-s12_research_bug_report-incredible-four-rep7 — s12_research_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 34 | — | 44 |
| batches_needed не учитывает последнюю неполную партию | bug | completed | Verified successfully | 5.3 | 10.9 | 26.4 |

Bug round-trips:

- `5dd0e888` batches_needed не учитывает последнюю неполную партию (activated 2026-10-28T20:20:02.283417+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 43.601 | 9.761 | 13.4044 | 26748 | 1615 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.357 | 1.026 | 1.1506 | 15054 | 568 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 9.057 | 1.4595 | 2.1145 | 35421 | 1542 |

Overall: 16 model requests, latency p50 1.4595 s / p95 11.4448 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-231913-s12_research_bug_report-incredible-four-rep7/`

### 20261028-232012-s12_research_bug_report-incredible-four-rep8 — s12_research_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 35.2 | — | 45 |
| batches_needed недосчитывает неполную партию (floor вместо ceil) | bug | completed | Verified successfully | 4.6 | 13 | 27.5 |

Bug round-trips:

- `e4f25860` batches_needed недосчитывает неполную партию (floor вместо ceil) (activated 2026-10-28T20:21:05.935890+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 44.598 | 10.6385 | 18.3964 | 21841 | 1588 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.218 | 0.7 | 1.3924 | 14730 | 438 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 9.912 | 1.367 | 2.1563 | 36634 | 1475 |

Overall: 16 model requests, latency p50 1.445 s / p95 13.1542 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232012-s12_research_bug_report-incredible-four-rep8/`

### 20261028-232021-s12_research_bug_report-incredible-four-rep9 — s12_research_bug_report × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 32.1 | — | 35.9 |
| batches_needed не учитывает неполную последнюю партию (не округляет вверх) | bug | completed | Verified successfully | 5.1 | 11.7 | 34.4 |

Bug round-trips:

- `e40ef607` batches_needed не учитывает неполную последнюю партию (не округляет вверх) (activated 2026-10-28T20:21:01.084769+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 35.626 | 9.1355 | 13.779 | 21777 | 1311 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 3.158 | 0.7035 | 1.1871 | 10504 | 387 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 10.309 | 1.399 | 2.1925 | 32251 | 1709 |

Overall: 15 model requests, latency p50 1.399 s / p95 13.7091 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232021-s12_research_bug_report-incredible-four-rep9/`

### 20261028-232021-s12_research_bug_report-regular-three-rep0 — s12_research_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed округляет вниз вместо вверх — теряется последняя неполная партия | bug | completed | Verified successfully | 8.7 | 8.5 | 18.4 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 3.8 | — | 5.1 |

Bug round-trips:

- `d6852ceb` batches_needed округляет вниз вместо вверх — теряется последняя неполная партия (activated 2026-10-28T20:20:30.818058+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 12.438 | 1.134 | 4.2605 | 25508 | 1111 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 7 | 6.352 | 0.939 | 1.1513 | 29481 | 743 |

Overall: 14 model requests, latency p50 0.9855 s / p95 3.2367 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232021-s12_research_bug_report-regular-three-rep0/`

### 20261028-232050-s12_research_bug_report-regular-three-rep1 — s12_research_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 6.5 | — | 7.3 |
| batches_needed теряет неполную партию: деление нацело вместо округления вверх | bug | completed | Verified successfully | 4.3 | 13.4 | 18.7 |

Bug round-trips:

- `f1c6fee6` batches_needed теряет неполную партию: деление нацело вместо округления вверх (activated 2026-10-28T20:21:02.366819+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 10.854 | 1.0795 | 2.5331 | 32243 | 1308 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 8.571 | 0.8985 | 1.8288 | 38084 | 827 |

Overall: 16 model requests, latency p50 0.953 s / p95 2.2795 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232050-s12_research_bug_report-regular-three-rep1/`

### 20261028-232122-s12_research_bug_report-regular-three-rep2 — s12_research_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed в dispatch/pricing.py делает округление вниз вместо округления вверх | bug | completed | Verified successfully | 4.2 | 12.7 | 17.8 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 7.8 | — | 8.5 |

Bug round-trips:

- `37edce13` batches_needed в dispatch/pricing.py делает округление вниз вместо округления вверх (activated 2026-10-28T20:21:42.118498+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 11.609 | 0.806 | 3.8357 | 29813 | 1278 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 10 | 7.845 | 0.6995 | 1.1915 | 43150 | 1072 |

Overall: 18 model requests, latency p50 0.7635 s / p95 2.2082 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232122-s12_research_bug_report-regular-three-rep2/`

### 20261028-232123-s12_research_bug_report-regular-three-rep3 — s12_research_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed округляет число партий вниз вместо вверх — теряется неполная партия | bug | completed | Verified successfully | 4 | 7.5 | 11.8 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 7.8 | — | 8.3 |

Bug round-trips:

- `1546bcc0` batches_needed округляет число партий вниз вместо вверх — теряется неполная партия (activated 2026-10-28T20:21:41.825323+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 11.213 | 1 | 4.232 | 25857 | 1212 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 5.195 | 0.868 | 1.2048 | 22750 | 625 |

Overall: 13 model requests, latency p50 0.928 s / p95 3.128 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232123-s12_research_bug_report-regular-three-rep3/`

### 20261028-232127-s12_research_bug_report-regular-three-rep4 — s12_research_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed округляет вниз и теряет последнюю неполную партию | bug | completed | Verified successfully | 4 | 6 | 11.2 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 6.1 | — | 7.2 |

Bug round-trips:

- `19e2abfa` batches_needed округляет вниз и теряет последнюю неполную партию (activated 2026-10-28T20:21:40.714743+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 9.86 | 0.905 | 3.1458 | 26732 | 1345 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.387 | 0.884 | 1.1432 | 18890 | 579 |

Overall: 12 model requests, latency p50 0.888 s / p95 2.5648 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232127-s12_research_bug_report-regular-three-rep4/`

### 20261028-232154-s12_research_bug_report-regular-three-rep5 — s12_research_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed отбрасывает неполную последнюю партию (floor вместо ceil) | bug | completed | Verified successfully | 5.5 | 6 | 12.3 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 4.1 | — | 5.1 |

Bug round-trips:

- `cac4d2ce` batches_needed отбрасывает неполную последнюю партию (floor вместо ceil) (activated 2026-10-28T20:22:04.073627+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 8.172 | 0.891 | 2.253 | 26878 | 1248 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.404 | 0.813 | 1.1706 | 25991 | 486 |

Overall: 12 model requests, latency p50 0.8765 s / p95 1.9455 s.
Recorder ↔ transcript cross-check: 12/12 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232154-s12_research_bug_report-regular-three-rep5/`

### 20261028-232155-s12_research_bug_report-regular-three-rep6 — s12_research_bug_report × regular-three

Reason: `settled but checks.py failed:
S12 checks FAILED:
- expected exactly 1 non-brief task with kind=bug (the research agent's create_bug_report product), found 2
- research transcript: create_bug_report description does not match the bug task's first prompt — the bug task was not created from THIS tool call`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| batches_needed в dispatch/pricing.py округляет вниз вместо вверх | bug | completed | Verified successfully | 3.1 | 11.2 | 14.8 |
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 5.4 | — | 6.6 |
| batches_needed в dispatch/pricing.py округляет вниз вместо вверх (нарушение контракта в докстринге) | bug | completed | Verified successfully | 3.8 | 7.5 | 14.9 |

Diagnostic (§7 S6, passive): 1 coder/tester activity overlap fact(s) recorded — informational, not a gate violation.

- {'source': 'transcripts', 'coder': 'bug:batches_needed в dispatch/pricing.py округляет вниз вместо вверх (нарушение контракта в докстринге)', 'tester': 'bug:batches_needed в dispatch/pricing.py округляет вниз вместо вверх round 0', 'at': '2026-10-28T20:22:18.274376+00:00', 'detail': 'coder message at 2026-10-28T20:22:18.274376+00:00 inside tester interval 2026-10-28T20:22:12.334844+00:00…2026-10-28T20:22:21.049078+00:00'}

Bug round-trips:

- `31370685` batches_needed в dispatch/pricing.py округляет вниз вместо вверх (activated 2026-10-28T20:22:06.677408+00:00)
- `a33d5056` batches_needed в dispatch/pricing.py округляет вниз вместо вверх (нарушение контракта в докстринге) (activated 2026-10-28T20:22:22.132787+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 14.542 | 0.898 | 3.378 | 34934 | 2143 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 13 | 13.237 | 0.915 | 1.8356 | 55325 | 1813 |

Overall: 23 model requests, latency p50 0.915 s / p95 2.9138 s.
Recorder ↔ transcript cross-check: 23/23 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232155-s12_research_bug_report-regular-three-rep6/`

### 20261028-232201-s12_research_bug_report-regular-three-rep7 — s12_research_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 5.3 | — | 6.5 |
| Исправить batches_needed в dispatch/pricing.py: целочисленное деление вместо округления вверх | bug | completed | Verified successfully | 4.7 | 9.2 | 15.2 |

Bug round-trips:

- `e3a43c80` Исправить batches_needed в dispatch/pricing.py: целочисленное деление вместо округления вверх (activated 2026-10-28T20:22:12.388589+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 11.601 | 1.267 | 3.412 | 26603 | 1673 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 5.531 | 0.856 | 1.289 | 23391 | 627 |

Overall: 13 model requests, latency p50 0.974 s / p95 3.028 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232201-s12_research_bug_report-regular-three-rep7/`

### 20261028-232218-s12_research_bug_report-regular-three-rep8 — s12_research_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 3.2 | — | 4.5 |
| batches_needed считает по floor вместо ceil — теряется последняя неполная партия | bug | completed | Verified successfully | 3.9 | 8.8 | 13.9 |

Bug round-trips:

- `db425b47` batches_needed считает по floor вместо ceil — теряется последняя неполная партия (activated 2026-10-28T20:22:27.069781+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 7.166 | 0.802 | 1.7401 | 25770 | 1207 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 6.121 | 1.045 | 1.3868 | 27580 | 882 |

Overall: 13 model requests, latency p50 0.97 s / p95 1.7272 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232218-s12_research_bug_report-regular-three-rep8/`

### 20261028-232229-s12_research_bug_report-regular-three-rep9 — s12_research_bug_report × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Проверьте dispatch/pricing.py на ошибки в логике | research | completed | — | 5.3 | — | 6.3 |
| batches_needed возвращает floor вместо ceil — теряется неполная последняя партия | bug | completed | Verified successfully | 3.6 | 5.9 | 10.8 |

Bug round-trips:

- `b2186eed` batches_needed возвращает floor вместо ceil — теряется неполная последняя партия (activated 2026-10-28T20:22:44.489043+00:00)

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 8.588 | 0.8535 | 1.9576 | 30874 | 1222 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.369 | 0.877 | 1.0108 | 18825 | 559 |

Overall: 13 model requests, latency p50 0.859 s / p95 1.8224 s.
Recorder ↔ transcript cross-check: 13/13 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232229-s12_research_bug_report-regular-three-rep9/`

### 20261028-232423-s13_research_feature-deepseek-v4-baseline-rep0 — s13_research_feature × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 26.5 | — | 32 |
| Заменить math.floor(...) на целочисленное деление // в датчиках telemetry | feature | completed | Verified successfully | 43.3 | 42.9 | 92.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 17 | 116.858 | 5.256 | 16.898 | 84270 | 4178 |

Overall: 17 model requests, latency p50 5.256 s / p95 16.898 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232423-s13_research_feature-deepseek-v4-baseline-rep0/`

### 20261028-232428-s13_research_feature-deepseek-v4-baseline-rep1 — s13_research_feature × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 27.4 | — | 33.8 |
| Заменить math.floor() на целочисленное деление // в пакете telemetry/ | feature | completed | Verified successfully | 39.1 | 49 | 94.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 17 | 121.087 | 5.356 | 16.8208 | 83610 | 4154 |

Overall: 17 model requests, latency p50 5.356 s / p95 16.8208 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232428-s13_research_feature-deepseek-v4-baseline-rep1/`

### 20261028-232454-s13_research_feature-deepseek-v4-baseline-rep2 — s13_research_feature × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // во всех модулях telemetry/ | feature | completed | Verified successfully | 52.2 | 37.3 | 96.9 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 18 | — | 25.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 109.049 | 4.612 | 18.1272 | 71459 | 3706 |

Overall: 16 model requests, latency p50 4.612 s / p95 18.1272 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232454-s13_research_feature-deepseek-v4-baseline-rep2/`

### 20261028-232631-s13_research_feature-deepseek-v4-baseline-rep3 — s13_research_feature × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Замена math.floor(...) на целочисленное деление // в модулях telemetry | feature | completed | Verified successfully | 43.6 | 68.6 | 117.6 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 23.7 | — | 29.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 18 | 140.654 | 5.9975 | 15.9979 | 95704 | 4989 |

Overall: 18 model requests, latency p50 5.9975 s / p95 15.9979 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232631-s13_research_feature-deepseek-v4-baseline-rep3/`

### 20261028-232639-s13_research_feature-deepseek-v4-baseline-rep4 — s13_research_feature × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // в telemetry/ | feature | completed | Verified successfully | 34.7 | 66.8 | 108.9 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 24.4 | — | 31.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 18 | 131.25 | 6.4205 | 15.5163 | 94632 | 4756 |

Overall: 18 model requests, latency p50 6.4205 s / p95 15.5163 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232639-s13_research_feature-deepseek-v4-baseline-rep4/`

### 20261028-232700-s13_research_feature-deepseek-v4-baseline-rep5 — s13_research_feature × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 22.8 | — | 27.7 |
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry | feature | completed | Verified successfully | 41.2 | 54.5 | 93.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 119.319 | 5.9505 | 15.5925 | 76925 | 4284 |

Overall: 16 model requests, latency p50 5.9505 s / p95 15.5925 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232700-s13_research_feature-deepseek-v4-baseline-rep5/`

### 20261028-232900-s13_research_feature-deepseek-v4-baseline-rep6 — s13_research_feature × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry | feature | completed | Verified successfully | 35.5 | 39.9 | 81 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 18.2 | — | 23.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 16 | 95.834 | 4.9755 | 14.55 | 70775 | 3657 |

Overall: 16 model requests, latency p50 4.9755 s / p95 14.55 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232900-s13_research_feature-deepseek-v4-baseline-rep6/`

### 20261028-232907-s13_research_feature-deepseek-v4-baseline-rep7 — s13_research_feature × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 18.6 | — | 23.1 |
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry | feature | completed | Verified successfully | 35.8 | 50.1 | 81.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 18 | 107.948 | 4.76 | 14.2079 | 86689 | 4197 |

Overall: 18 model requests, latency p50 4.76 s / p95 14.2079 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232907-s13_research_feature-deepseek-v4-baseline-rep7/`

### 20261028-232910-s13_research_feature-deepseek-v4-baseline-rep8 — s13_research_feature × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry | feature | completed | Verified successfully | 29.8 | 41.7 | 76.6 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 27.5 | — | 33.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 18 | 106.44 | 4.7445 | 14.897 | 86362 | 3993 |

Overall: 18 model requests, latency p50 4.7445 s / p95 14.897 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232910-s13_research_feature-deepseek-v4-baseline-rep8/`

### 20261028-233049-s13_research_feature-deepseek-v4-baseline-rep9 — s13_research_feature × deepseek-v4-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 20.3 | — | 24.5 |
| Replace math.floor(...) with integer division // in telemetry sensors | feature | completed | Verified successfully | 47.2 | 39.1 | 90.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 14 | 112.665 | 6.0995 | 19.3243 | 63200 | 3882 |

Overall: 14 model requests, latency p50 6.0995 s / p95 19.3243 s.
Recorder ↔ transcript cross-check: 14/14 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233049-s13_research_feature-deepseek-v4-baseline-rep9/`

### 20261028-232236-s13_research_feature-glm-5.3-baseline-rep0 — s13_research_feature × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 7.1 | — | 7.9 |
| Заменить math.floor(...) на целочисленное деление // в модулях telemetry/ | feature | completed | Verified successfully | 5.1 | 10 | 15.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 19 | 20.314 | 0.921 | 1.7879 | 78555 | 1997 |

Overall: 19 model requests, latency p50 0.921 s / p95 1.7879 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232236-s13_research_feature-glm-5.3-baseline-rep0/`

### 20261028-232242-s13_research_feature-glm-5.3-baseline-rep1 — s13_research_feature × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // во всех модулях telemetry/ | feature | completed | Verified successfully | 7.1 | 6.8 | 14.7 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 5.4 | — | 6.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 17 | 16.861 | 0.839 | 1.6024 | 76413 | 2359 |

Overall: 17 model requests, latency p50 0.839 s / p95 1.6024 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232242-s13_research_feature-glm-5.3-baseline-rep1/`

### 20261028-232257-s13_research_feature-glm-5.3-baseline-rep2 — s13_research_feature × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 4.7 | — | 5.5 |
| Заменить math.floor(...) на целочисленное деление // во всех модулях пакета telemetry/ | feature | completed | Verified successfully | 4.5 | 10.5 | 15.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 19 | 18.096 | 0.914 | 1.7026 | 83841 | 2374 |

Overall: 19 model requests, latency p50 0.914 s / p95 1.7026 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232257-s13_research_feature-glm-5.3-baseline-rep2/`

### 20261028-232307-s13_research_feature-glm-5.3-baseline-rep3 — s13_research_feature × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // во всех модулях telemetry/ | feature | completed | Verified successfully | 7.2 | 10.1 | 18.2 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 5.1 | — | 5.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 18 | 21.441 | 1.061 | 2.1045 | 76227 | 2124 |

Overall: 18 model requests, latency p50 1.061 s / p95 2.1045 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232307-s13_research_feature-glm-5.3-baseline-rep3/`

### 20261028-232310-s13_research_feature-glm-5.3-baseline-rep4 — s13_research_feature × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 4.7 | — | 5.7 |
| Заменить math.floor(...) на целочисленное деление // в модулях пакета telemetry | feature | completed | Verified successfully | 4.7 | 7.8 | 13.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 16 | 16.655 | 0.912 | 1.921 | 64492 | 2139 |

Overall: 16 model requests, latency p50 0.912 s / p95 1.921 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232310-s13_research_feature-glm-5.3-baseline-rep4/`

### 20261028-232324-s13_research_feature-glm-5.3-baseline-rep5 — s13_research_feature × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на оператор целочисленного деления // в telemetry/ | feature | completed | Verified successfully | 5.7 | 8.4 | 14.9 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 5.6 | — | 6.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 20 | 17.855 | 0.729 | 1.5128 | 83976 | 2057 |

Overall: 20 model requests, latency p50 0.729 s / p95 1.5128 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232324-s13_research_feature-glm-5.3-baseline-rep5/`

### 20261028-232336-s13_research_feature-glm-5.3-baseline-rep6 — s13_research_feature × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 5 | — | 6 |
| Заменить math.floor(...) на целочисленное деление // в датчиках пакета telemetry/ | feature | completed | Verified successfully | 14.2 | 14.6 | 30.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 28 | 30.424 | 0.8255 | 1.8523 | 123904 | 2725 |

Overall: 28 model requests, latency p50 0.8255 s / p95 1.8523 s.
Recorder ↔ transcript cross-check: 28/28 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232336-s13_research_feature-glm-5.3-baseline-rep6/`

### 20261028-232340-s13_research_feature-glm-5.3-baseline-rep7 — s13_research_feature × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // в telemetry/ | feature | completed | Verified successfully | 9.9 | 14.5 | 25.8 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 5.7 | — | 6.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 19 | 26.42 | 1.288 | 2.7149 | 80859 | 3016 |

Overall: 19 model requests, latency p50 1.288 s / p95 2.7149 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232340-s13_research_feature-glm-5.3-baseline-rep7/`

### 20261028-232353-s13_research_feature-glm-5.3-baseline-rep8 — s13_research_feature × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry/ | feature | completed | Verified successfully | 13.5 | 7 | 20.9 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 5.8 | — | 6.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 17 | 22.471 | 0.985 | 2.9908 | 68354 | 2268 |

Overall: 17 model requests, latency p50 0.985 s / p95 2.9908 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232353-s13_research_feature-glm-5.3-baseline-rep8/`

### 20261028-232419-s13_research_feature-glm-5.3-baseline-rep9 — s13_research_feature × glm-5.3-baseline

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 10.3 | — | 11 |
| Заменить math.floor(...) на целочисленное деление // во всех модулях telemetry/ | feature | completed | Verified successfully | 6.9 | 9.1 | 16.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 18 | 23.525 | 0.8935 | 2.6989 | 75048 | 1983 |

Overall: 18 model requests, latency p50 0.8935 s / p95 2.6989 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-232419-s13_research_feature-glm-5.3-baseline-rep9/`

### 20261028-233104-s13_research_feature-incredible-four-rep0 — s13_research_feature × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 25.9 | — | 32.3 |
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry | feature | completed | Verified successfully | 9.1 | 18.6 | 35.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 32.114 | 7.725 | 12.7846 | 20122 | 1065 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 5.669 | 0.8415 | 1.5272 | 23200 | 773 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 16.241 | 1.441 | 4.3426 | 41104 | 1724 |

Overall: 18 model requests, latency p50 1.441 s / p95 9.2874 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233104-s13_research_feature-incredible-four-rep0/`

### 20261028-233105-s13_research_feature-incredible-four-rep1 — s13_research_feature × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 22 | — | 27.4 |
| Заменить math.floor(...) на целочисленное деление // во всех датчиках telemetry/ | feature | completed | Verified successfully | 4.2 | 17.1 | 26.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 27.157 | 5.9965 | 11.2845 | 20199 | 962 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 4 | 4.23 | 0.952 | 1.4934 | 15281 | 480 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 14.589 | 1.491 | 4.5075 | 38305 | 1546 |

Overall: 15 model requests, latency p50 1.587 s / p95 7.8949 s.
Recorder ↔ transcript cross-check: 15/15 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233105-s13_research_feature-incredible-four-rep1/`

### 20261028-233201-s13_research_feature-incredible-four-rep2 — s13_research_feature × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 28.9 | — | 36.1 |
| Заменить math.floor(...) на целочисленное деление // в telemetry | feature | completed | Verified successfully | 7.8 | 22.2 | 40.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 35.805 | 8.089 | 15.0679 | 21277 | 1235 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 10.197 | 1.2995 | 3.269 | 26388 | 1700 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 16.748 | 2.586 | 2.9737 | 50843 | 2030 |

Overall: 17 model requests, latency p50 2.606 s / p95 11.6574 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233201-s13_research_feature-incredible-four-rep2/`

### 20261028-233211-s13_research_feature-incredible-four-rep3 — s13_research_feature × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 21.2 | — | 24.9 |
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry | feature | completed | Verified successfully | 10 | 16.3 | 31.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 24.676 | 5.666 | 10.6663 | 19811 | 815 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 6 | 10.475 | 1.576 | 2.8805 | 22996 | 1003 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 6 | 13.915 | 1.7825 | 4.5405 | 39290 | 1900 |

Overall: 16 model requests, latency p50 1.9715 s / p95 7.3795 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233211-s13_research_feature-incredible-four-rep3/`

### 20261028-233258-s13_research_feature-incredible-four-rep4 — s13_research_feature × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 24.9 | — | 31.1 |
| Заменить math.floor(...) на целочисленное деление // в telemetry/ | feature | completed | Verified successfully | 14.1 | 21 | 43.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 30.842 | 6.539 | 14.2838 | 19865 | 922 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 12.062 | 1.013 | 1.5854 | 49328 | 1663 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 16.468 | 2.0585 | 2.8582 | 50927 | 2256 |

Overall: 24 model requests, latency p50 1.435 s / p95 8.1 s.
Recorder ↔ transcript cross-check: 24/24 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233258-s13_research_feature-incredible-four-rep4/`

### 20261028-233309-s13_research_feature-incredible-four-rep5 — s13_research_feature × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 23.9 | — | 27.5 |
| Заменить math.floor(...) на целочисленное деление // в telemetry/ | feature | completed | Verified successfully | 6.1 | 24.2 | 33.7 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 27.181 | 4.9185 | 13.2532 | 19930 | 909 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 7 | 6.532 | 0.807 | 1.5507 | 25937 | 1005 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 20.537 | 2.442 | 4.3381 | 52403 | 3045 |

Overall: 19 model requests, latency p50 1.779 s / p95 6.6142 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233309-s13_research_feature-incredible-four-rep5/`

### 20261028-233320-s13_research_feature-incredible-four-rep6 — s13_research_feature × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 24.9 | — | 29.3 |
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry | feature | completed | Verified successfully | 8.4 | 21.9 | 34.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 29.085 | 5.5545 | 13.1599 | 20346 | 1110 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 6.059 | 1.079 | 1.6854 | 19323 | 738 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 8 | 20.493 | 2.6885 | 4.3287 | 47650 | 2900 |

Overall: 17 model requests, latency p50 2.613 s / p95 7.7864 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233320-s13_research_feature-incredible-four-rep6/`

### 20261028-233412-s13_research_feature-incredible-four-rep7 — s13_research_feature × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry | feature | completed | Verified successfully | 9.7 | 12.9 | 31 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 29.7 | — | 34.8 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 4 | 34.512 | 7.194 | 15.4685 | 20369 | 1159 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 9.933 | 0.897 | 1.6492 | 38200 | 1209 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 10.907 | 1.709 | 1.9484 | 42004 | 1409 |

Overall: 20 model requests, latency p50 1.6175 s / p95 9.7702 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233412-s13_research_feature-incredible-four-rep7/`

### 20261028-233418-s13_research_feature-incredible-four-rep8 — s13_research_feature × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 27.7 | — | 34.3 |
| Заменить math.floor(...) на целочисленное деление // в модулях telemetry | feature | completed | Verified successfully | 4.3 | 16.9 | 29.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 34.053 | 4.893 | 13.6872 | 26258 | 1318 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.573 | 0.917 | 1.045 | 19020 | 784 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 7 | 13.587 | 1.966 | 2.993 | 40763 | 1769 |

Overall: 17 model requests, latency p50 1.966 s / p95 9.8988 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233418-s13_research_feature-incredible-four-rep8/`

### 20261028-233427-s13_research_feature-incredible-four-rep9 — s13_research_feature × incredible-four

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 30.1 | — | 36.4 |
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry/ | feature | completed | Verified successfully | 4.4 | 24.5 | 35.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-large-thinking@https://api-copilot.x5.ru/aigw/v1 | 5 | 36.127 | 4.645 | 15.5984 | 26334 | 1294 |
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 5 | 4.578 | 0.871 | 1.3246 | 19609 | 929 |
| x5-airun-medium-thinking@https://api-copilot.x5.ru/aigw/v1 | 11 | 22.156 | 2.029 | 2.784 | 81043 | 3795 |

Overall: 21 model requests, latency p50 2.029 s / p95 6.976 s.
Recorder ↔ transcript cross-check: 21/21 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233427-s13_research_feature-incredible-four-rep9/`

### 20261028-233520-s13_research_feature-regular-three-rep0 — s13_research_feature × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на оператор целочисленного деления // в пакете telemetry/ | feature | completed | Verified successfully | 5.8 | 10.3 | 17 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 4.6 | — | 5.3 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 11.045 | 0.8945 | 2.0714 | 44366 | 2177 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 8.41 | 0.904 | 1.9556 | 36267 | 858 |

Overall: 18 model requests, latency p50 0.8945 s / p95 2.2829 s.
Recorder ↔ transcript cross-check: 18/18 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233520-s13_research_feature-regular-three-rep0/`

### 20261028-233521-s13_research_feature-regular-three-rep1 — s13_research_feature × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // во всех модулях пакета telemetry/ | feature | completed | Verified successfully | 10.8 | 9.5 | 21.4 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 6.4 | — | 7.5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 13 | 17.279 | 1.059 | 2.5942 | 60135 | 2181 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 7 | 7.288 | 1.084 | 1.4165 | 40064 | 750 |

Overall: 20 model requests, latency p50 1.0715 s / p95 2.2764 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233521-s13_research_feature-regular-three-rep1/`

### 20261028-233540-s13_research_feature-regular-three-rep2 — s13_research_feature × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 4.7 | — | 5.6 |
| Заменить math.floor(...) на целочисленное деление // во всех модулях пакета telemetry/ | feature | completed | Verified successfully | 6 | 10.3 | 16.9 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 12 | 12.242 | 0.8485 | 1.652 | 52279 | 1861 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 7.693 | 0.835 | 1.5886 | 33007 | 954 |

Overall: 20 model requests, latency p50 0.8485 s / p95 1.6786 s.
Recorder ↔ transcript cross-check: 20/20 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233540-s13_research_feature-regular-three-rep2/`

### 20261028-233552-s13_research_feature-regular-three-rep3 — s13_research_feature × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 4.3 | — | 5.3 |
| Заменить math.floor(...) на целочисленное деление // в модулях пакета telemetry/ | feature | completed | Verified successfully | 5.5 | 11 | 16.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 10.881 | 0.9255 | 1.7784 | 43897 | 2062 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 7 | 7.005 | 0.837 | 1.6107 | 36824 | 514 |

Overall: 17 model requests, latency p50 0.894 s / p95 1.858 s.
Recorder ↔ transcript cross-check: 17/17 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233552-s13_research_feature-regular-three-rep3/`

### 20261028-233558-s13_research_feature-regular-three-rep4 — s13_research_feature × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // в telemetry/ | feature | completed | Verified successfully | 4.9 | 10.5 | 16.4 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 5.8 | — | 6.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 8 | 11.553 | 1.057 | 2.7237 | 36164 | 2311 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 8.251 | 0.99 | 1.5281 | 41617 | 663 |

Overall: 16 model requests, latency p50 1.01 s / p95 2.4125 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233558-s13_research_feature-regular-three-rep4/`

### 20261028-233609-s13_research_feature-regular-three-rep5 — s13_research_feature × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // в пакете telemetry | feature | completed | Verified successfully | 5.4 | 9.6 | 15.9 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 4.2 | — | 5 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 9 | 10.442 | 1.172 | 1.7758 | 39446 | 2039 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 10 | 6.976 | 0.687 | 0.9083 | 42498 | 665 |

Overall: 19 model requests, latency p50 0.779 s / p95 1.6618 s.
Recorder ↔ transcript cross-check: 19/19 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233609-s13_research_feature-regular-three-rep5/`

### 20261028-233620-s13_research_feature-regular-three-rep6 — s13_research_feature × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // во всех модулях пакета telemetry/ | feature | completed | Verified successfully | 6.7 | 7.1 | 14.4 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 4.4 | — | 5.2 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 10.205 | 0.8935 | 1.8249 | 41852 | 1492 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 5.309 | 0.794 | 1.15 | 23997 | 713 |

Overall: 16 model requests, latency p50 0.839 s / p95 1.5495 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233620-s13_research_feature-regular-three-rep6/`

### 20261028-233628-s13_research_feature-regular-three-rep7 — s13_research_feature × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на оператор целочисленного деления // в пакете telemetry/ | feature | completed | Verified successfully | 9.1 | 8.6 | 18.4 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 4.5 | — | 5.1 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 14 | 12.768 | 0.802 | 1.503 | 58271 | 1651 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 8 | 6.685 | 0.699 | 1.284 | 32516 | 720 |

Overall: 22 model requests, latency p50 0.7745 s / p95 1.4402 s.
Recorder ↔ transcript cross-check: 22/22 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233628-s13_research_feature-regular-three-rep7/`

### 20261028-233637-s13_research_feature-regular-three-rep8 — s13_research_feature × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 5.6 | — | 6.4 |
| Заменить math.floor(...) на целочисленное деление // во всех модулях пакета telemetry/ | feature | completed | Verified successfully | 6.5 | 7.1 | 14.6 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 13.096 | 1.291 | 1.9542 | 44005 | 2002 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 4.998 | 0.8465 | 1.0105 | 24469 | 566 |

Overall: 16 model requests, latency p50 1.0615 s / p95 1.851 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233637-s13_research_feature-regular-three-rep8/`

### 20261028-233646-s13_research_feature-regular-three-rep9 — s13_research_feature × regular-three

Reason: `settled`

| task | kind | status | verification | dev s | testing s | total s |
|---|---|---|---|---|---|---|
| Заменить math.floor(...) на целочисленное деление // в telemetry/ | feature | completed | Verified successfully | 5.6 | 6.9 | 13.8 |
| Составьте задачу на перевод телеметрии на целочисленное деление | research | completed | — | 6.3 | — | 7.4 |

User-simulator interventions: 0 (start: 1)

Model usage per role (recorder):

| role | requests | latency total s | latency p50 s | latency p95 s | input tok | output tok |
|---|---|---|---|---|---|---|
| x5-airun-code-large@https://api-copilot.x5.ru/aigw/v1 | 10 | 11.664 | 1.0745 | 1.9378 | 43660 | 1936 |
| x5-airun-medium@https://api-copilot.x5.ru/aigw/v1 | 6 | 4.481 | 0.746 | 0.9238 | 21913 | 423 |

Overall: 16 model requests, latency p50 0.9125 s / p95 1.831 s.
Recorder ↔ transcript cross-check: 16/16 transcript responses matched, 0 unmatched recorder entries (compaction requests, §1.5) — no unexplained discrepancies.

Artifacts: `20261028-233646-s13_research_feature-regular-three-rep9/`


## Glossary

Meaning of the codes in the tables above:

- gate `ok` — the coder/tester activity check (§7 S6) ran: tester rounds are present; coder/tester interval overlaps, if any, are recorded as PASSIVE diagnostics in metrics.json ('overlaps') — in multi-task runs the coder legitimately works on other tasks while the tester verifies one, so they are never a violation
- gate `commit-yes` — report_committed (s9): the measured git_commit_docs discipline — the run's report was committed; a METRIC, not a verdict gate (a `no` pair can still be a green run)
- gate `commit-no` — report_committed (s9): the measured git_commit_docs discipline — the report was NOT committed; a METRIC, not a verdict gate (a `no` pair can still be a green run)
- gate `commit-mixed` — report_committed (s9): the pair's repeats disagree on whether git_commit_docs committed the report
- stability `faults×N` — faults injected by the proxy fault script (s7 [proxy] runs / --use-proxy); the retries they caused appear alongside as net-retry
- stability `compact-fail×N` — compaction failed: drcode does not abort — it disables the compaction gate (`_compaction_failed`) and continues with the UNCOMPRESSED history (summaries may be missing from transcripts)
- stability `tester-fail×N` — tester failures
- stability `net-retry×N` — drcode retried a failed model request
- stability `unfinished` — task not finished by the end of the run
- stability `stuck-clarif` — task left pending clarification
- stability `excluded` — task excluded from the queue
- stability `clean` — none of the above
- combo `◉` — the pair is on its scenario's Pareto frontier over (median wall-time, median cost $) among the green pairs — no green pair of the scenario is both as fast and as cheap; a pair without a price is frontier-eligible on the time axis only

Quality ranking notes:

- `pass rate` — the share of the pair's repeats with verdict `green` (the `verdicts` column already lists all outcomes seen; a pair is only as good as its worst repeat).
- `score (α·t+β$)` — cost = α·t_norm + β·m_norm, where t_norm / m_norm divide the pair's median wall-time / median cost by the scenario's best GREEN repeat (the fastest / cheapest green run; it scores 1.0, so scores are comparable across scenarios); α is the `--time-weight` (default 0 = money only), β is fixed at 1. Only the pair's GREEN repeats are scored (red repeats are skipped), so any pair with at least one green repeat gets a score; a fully failed pair renders `—`. The cell shows the median over the scored repeats of each repeat's normalized score, with the spread.
- With 1–3 repeats the score is a RANKING, not a ratio: treat it as an ordinal 'which pair is better', never as '2× better'.
- `cost $ (med)` is computed only when every model referenced by the combo has both `price_input` and `price_output` in the matrix given via `--matrix`; unpriced pairs render `—` and rank after priced ones (by wall-time) within the same outcome class and pass rate.
