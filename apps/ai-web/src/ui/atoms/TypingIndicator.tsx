export function TypingIndicator() {
    return (
        <div className="flex justify-start">
            <div className="bg-secondary border border-border rounded-2xl px-4 py-3">
                <div className="flex gap-1.5 items-center h-5">
                    <span className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-bounce [animation-delay:-0.3s]" />
                    <span className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-bounce [animation-delay:-0.15s]" />
                    <span className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-bounce" />
                </div>
            </div>
        </div>
    )
}
