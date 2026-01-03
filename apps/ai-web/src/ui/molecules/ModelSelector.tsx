import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

interface ModelSelectorProps {
    value: string
    onChange: (model: string) => void
    models: Array<{ name: string; provider: string }>
    disabled?: boolean
}

export function ModelSelector({ value, onChange, models, disabled }: ModelSelectorProps) {
    return (
        <div className="flex items-center gap-3">
            <label htmlFor="model-select" className="text-sm font-medium text-foreground">
                Model:
            </label>
            <Select value={value} onValueChange={onChange} disabled={disabled}>
                <SelectTrigger className="w-[280px]" id="model-select">
                    <SelectValue placeholder="Select a model" />
                </SelectTrigger>
                <SelectContent>
                    {models.map((model) => (
                        <SelectItem key={model.name} value={model.name}>
                            <span className="font-mono text-sm">{model.name}</span>
                            <span className="ml-2 text-xs text-muted-foreground">({model.provider})</span>
                        </SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </div>
    )
}
