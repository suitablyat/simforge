"use client"

import { useActionState, useEffect, useRef } from "react"
import { submitQuickSim, type SubmitState } from "./actions/submitQuickSim"

export default function QuickSimForm() {
  const initialState: SubmitState = { ok: false, message: "" }
  const [state, action, isPending] = useActionState(submitQuickSim, initialState)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (state.errors?.simc && textareaRef.current) {
      textareaRef.current.focus()
    }
  }, [state])

  return (
    <form action={action} className="grid gap-4">
      <label htmlFor="simc" className="text-sm font-medium">
        .simc
      </label>

      <textarea
        id="simc"
        name="simc"
        ref={textareaRef}
        required
        minLength={20}
        maxLength={100000}
        placeholder="paste your .simc here…"
        className="bg-[#0f1521] border border-white/10 rounded-2xl p-4 leading-relaxed min-h-[240px] outline-none focus:ring-2 focus:ring-white/20"
      />

      {state.errors?.simc && (
        <p className="text-red-300 text-sm">{state.errors.simc}</p>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="rounded-2xl px-5 py-3 bg-white text-black font-medium disabled:opacity-60"
      >
        {isPending ? "Submitting…" : "Run Quick Sim"}
      </button>

      {state.message && (
        <p className={`text-sm ${state.ok ? "text-green-300" : "text-red-300"}`}>
          {state.message}
        </p>
      )}
    </form>
  )
}
