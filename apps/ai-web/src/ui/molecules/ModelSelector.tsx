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
        <div className="flex items-center gap-2 sm:gap-3 min-w-0">
            <label htmlFor="model-select" className="text-sm font-medium text-foreground hidden sm:inline">
                Model:
            </label>
            <Select value={value} onValueChange={onChange} disabled={disabled}>
                <SelectTrigger className="w-[180px] sm:w-[240px]" id="model-select">
                    <SelectValue placeholder="選擇模型" />
                </SelectTrigger>
                <SelectContent
                    className="w-[180px] sm:w-[240px] max-h-[300px]"
                    position="popper"
                    sideOffset={4}
                >
                    {models.map((model) => (
                        <SelectItem
                            key={model.name}
                            value={model.name}
                        >
                            <span className="font-mono text-sm truncate" title={model.name}>
                                {model.name}
                            </span>
                        </SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </div>
    )
}
