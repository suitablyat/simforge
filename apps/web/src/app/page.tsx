import QuickSimForm from "./quick-sim-form"

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <section className="mx-auto max-w-3xl px-4 py-16">
        <header className="mb-10">
          <h1 className="text-4xl font-semibold tracking-tight">Simforge</h1>
          <p className="mt-2 opacity-80">
            Paste your <code>.simc</code> and run a quick simulation.
          </p>
        </header>
        <QuickSimForm />
      </section>
      <footer className="py-10 text-center opacity-60 text-sm">
        SSR ✓ • Tailwind ✓ • Quick Sim Form ✓
      </footer>
    </main>
  )
}
