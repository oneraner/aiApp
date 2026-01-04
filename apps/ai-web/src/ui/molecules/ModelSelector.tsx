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
                <SelectTrigger className="w-[200px] sm:w-[280px]" id="model-select">
                    <SelectValue placeholder="Select a model" />
                </SelectTrigger>
                <SelectContent
                    className="bg-white w-[200px] sm:w-[280px] max-h-[300px] overflow-y-auto"
                    position="popper"
                    sideOffset={4}
                >
                    {models.map((model) => (
                        <SelectItem
                            key={model.name}
                            value={model.name}
                            className="cursor-pointer px-2 py-1.5"
                        >
                            <div className="w-full overflow-hidden line-clamp-1">
                                <span
                                    className="font-mono text-sm text-gray-900 block"
                                    title={model.name}
                                >
                                    {model.name}
                                </span>
                            </div>
                        </SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </div>
    )
}
