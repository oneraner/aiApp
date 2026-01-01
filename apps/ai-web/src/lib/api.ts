// src/lib/api.ts
export async function triggerAI(payload: {
  model: string
  contents: { type: string; content: string }[]
}) {
  const res = await fetch('http://localhost:8000/api/v1/trigger', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) throw new Error('trigger failed')
  return res.json() as Promise<{ job_id: string }>
}

export function streamAI(
  jobId: string,
  onChunk: (chunk: string) => void,
) {
  const es = new EventSource(
    `http://localhost:8000/api/v1/stream/${jobId}`,
  )

  es.onmessage = (e) => {
    onChunk(e.data)
  }

  es.onerror = () => {
    es.close()
  }

  return () => es.close()
}
