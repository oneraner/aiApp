import { useState, useEffect } from 'react'
import { getModels } from '../api/chat-api'

interface Model {
    name: string
    provider: string
    capabilities: string[]
}

export function useModels() {
    const [models, setModels] = useState<Model[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function fetchModels() {
            try {
                const data = await getModels()
                setModels(data)
            } catch (err) {
                setError(err instanceof Error ? err.message : '載入模型失敗')
            } finally {
                setLoading(false)
            }
        }

        fetchModels()
    }, [])

    return { models, loading, error }
}
