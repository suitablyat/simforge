from worker.simc_runner import run_simc
print(run_simc("iterations=1\noptimal_raid=1\narmory=eu,blackmoore,suitw", channel="latest").keys())
