"use server"

import { z } from "zod"

export type SubmitState = {
  ok: boolean
  message: string
  errors?: { simc?: string }
}

export async function submitQuickSim(
  prevState: SubmitState,
  formData: FormData
): Promise<SubmitState> {
  const schema = z.object({
    simc: z
      .string()
      .min(20, "Your .simc is too short (min 20 chars).")
      .max(100_000, "Your .simc is too long (max 100k chars)."),
  })

  const parsed = schema.safeParse({
    simc: formData.get("simc")?.toString() ?? "",
  })

  if (!parsed.success) {
    const simc =
      parsed.error.flatten().fieldErrors.simc?.[0] ?? "Invalid input."
    return { ok: false, message: "Validation failed.", errors: { simc } }
  }

  // TODO: Worker/API triggern
  return { ok: true, message: "Submitted successfully." }
}
