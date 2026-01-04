import { ScrollArea } from "@/components/ui/scroll-area"
import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogTitle,
} from "@/components/ui/dialog"
import { MessageSquare, Trash2, Loader2 } from "lucide-react"
import { useState } from "react"
import { useConversations } from "@/features/chat/hooks/useConversations"

interface ConversationSidebarProps {
    currentConversationId: string | null
    onSelectConversation: (id: string) => void
    onNewConversation: () => void
}

export function ConversationSidebar({
    currentConversationId,
    onSelectConversation,
    onNewConversation,
}: ConversationSidebarProps) {
    const { conversations, loading, deleteConversation } = useConversations()
    const [deleteDialogId, setDeleteDialogId] = useState<string | null>(null)
    const [deleting, setDeleting] = useState(false)

    const handleDelete = async () => {
        if (!deleteDialogId) return

        setDeleting(true)
        try {
            await deleteConversation(deleteDialogId)
            setDeleteDialogId(null)

            // If deleting current conversation, create new one
            if (deleteDialogId === currentConversationId) {
                onNewConversation()
            }
        } catch (error) {
            console.error('Failed to delete conversation:', error)
        } finally {
            setDeleting(false)
        }
    }

    const formatDate = (dateString: string) => {
        // Backend returns UTC time, append 'Z' if not present to ensure correct parsing
        const isoString = dateString.endsWith('Z') ? dateString : dateString + 'Z'
        const date = new Date(isoString)
        const now = new Date()
        const diffMs = now.getTime() - date.getTime()
        const diffMins = Math.floor(diffMs / 60000)
        const diffHours = Math.floor(diffMs / 3600000)
        const diffDays = Math.floor(diffMs / 86400000)

        if (diffMins < 1) return 'Just now'
        if (diffMins < 60) return `${diffMins}m ago`
        if (diffHours < 24) return `${diffHours}h ago`
        if (diffDays < 7) return `${diffDays}d ago`
        return date.toLocaleDateString()
    }

    return (
        <div className="h-full flex flex-col">
            {/* Header - Match main area header height (h-16) */}
            <div className="h-16 px-4 border-b flex items-center flex-shrink-0">
                <h2 className="font-semibold">Conversations</h2>
            </div>

            {/* Conversation List */}
            <ScrollArea className="flex-1">
                <div className="p-2 space-y-1">
                    {loading && (
                        <div className="flex items-center justify-center py-8">
                            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
                        </div>
                    )}

                    {!loading && conversations.length === 0 && (
                        <div className="text-center py-8 text-sm text-muted-foreground">
                            No conversations yet
                        </div>
                    )}

                    {conversations.map((conv) => (
                        <div
                            key={conv.id}
                            className={`group relative rounded-lg p-3 cursor-pointer transition-colors ${conv.id === currentConversationId
                                ? 'bg-secondary'
                                : 'hover:bg-secondary/50'
                                }`}
                            onClick={() => onSelectConversation(conv.id)}
                        >
                            <div className="flex items-start justify-between gap-2">
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2 mb-1">
                                        <MessageSquare className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
                                        <span className="text-xs text-muted-foreground">
                                            {formatDate(conv.updated_at)}
                                        </span>
                                    </div>
                                    <p className="text-sm font-medium truncate">
                                        Conversation {conv.message_count > 0 ? `(${conv.message_count} messages)` : '(empty)'}
                                    </p>
                                </div>

                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="opacity-0 group-hover:opacity-100 transition-opacity h-8 w-8"
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        setDeleteDialogId(conv.id)
                                    }}
                                >
                                    <Trash2 className="h-4 w-4 text-destructive" />
                                </Button>
                            </div>
                        </div>
                    ))}
                </div>
            </ScrollArea>


            {/* Delete Confirmation Dialog */}
            <Dialog open={!!deleteDialogId} onOpenChange={(open) => !open && setDeleteDialogId(null)}>
                <DialogContent className="sm:max-w-md bg-white p-0 overflow-hidden">
                    {/* Warning Header */}
                    <div className="bg-[#dd9222] px-6 py-4">
                        <DialogTitle className="flex items-center gap-2 text-white">
                            <Trash2 className="h-5 w-5" />
                            Delete Conversation
                        </DialogTitle>
                    </div>

                    {/* Content */}
                    <div className="px-6 py-4">
                        <DialogDescription className="text-base text-gray-700">
                            Are you sure you want to delete this conversation? This action cannot be undone.
                        </DialogDescription>
                    </div>

                    {/* Footer */}
                    <DialogFooter className="px-6 py-4 border-t">
                        <Button
                            variant="outline"
                            onClick={() => setDeleteDialogId(null)}
                            disabled={deleting}
                        >
                            Cancel
                        </Button>
                        <Button
                            onClick={handleDelete}
                            disabled={deleting}
                            className="bg-[#cc334d] hover:bg-[#a3293d] text-white font-medium"
                        >
                            {deleting && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
                            Delete
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    )
}
