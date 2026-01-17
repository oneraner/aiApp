import { ScrollArea } from "@/components/ui/scroll-area"
import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogTitle,
} from "@/components/ui/dialog"
import { MessageSquare, Trash2, Loader2, Plus } from "lucide-react"
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
        const isoString = dateString.endsWith('Z') ? dateString : `${dateString}Z`
        const date = new Date(isoString)
        const now = new Date()
        const diffMs = now.getTime() - date.getTime()
        const diffMins = Math.floor(diffMs / 60000)
        const diffHours = Math.floor(diffMs / 3600000)
        const diffDays = Math.floor(diffMs / 86400000)

        if (diffMins < 1) return '剛剛'
        if (diffMins < 60) return `${diffMins} 分鐘前`
        if (diffHours < 24) return `${diffHours} 小時前`
        if (diffDays < 7) return `${diffDays} 天前`
        return date.toLocaleDateString()
    }

    return (
        <div className="h-full flex flex-col bg-card">
            {/* Header */}
            <div className="h-16 px-4 border-b border-border flex items-center justify-between flex-shrink-0">
                <h2 className="font-semibold text-foreground">對話紀錄</h2>
                <Button
                    variant="ghost"
                    size="icon"
                    onClick={onNewConversation}
                    className="h-8 w-8 text-primary hover:text-primary hover:bg-primary/10"
                    aria-label="新增對話"
                >
                    <Plus className="h-4 w-4" />
                </Button>
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
                            還沒有對話紀錄
                        </div>
                    )}

                    {conversations.map((conv) => (
                        <div
                            key={conv.id}
                            className={`group relative rounded-lg p-3 cursor-pointer transition-all duration-200 ${conv.id === currentConversationId
                                ? 'bg-primary/10 border border-primary/20'
                                : 'hover:bg-secondary border border-transparent'
                                }`}
                            onClick={() => onSelectConversation(conv.id)}
                        >
                            <div className="flex items-start justify-between gap-2">
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2 mb-1">
                                        <MessageSquare className={`h-3.5 w-3.5 flex-shrink-0 ${conv.id === currentConversationId ? 'text-primary' : 'text-muted-foreground'}`} />
                                        <span className="text-xs text-muted-foreground">
                                            {formatDate(conv.updated_at)}
                                        </span>
                                    </div>
                                    <p className="text-sm font-medium truncate text-foreground">
                                        對話 {conv.message_count > 0 ? `(${conv.message_count} 則訊息)` : '(空)'}
                                    </p>
                                </div>

                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="opacity-0 group-hover:opacity-100 transition-opacity h-7 w-7 hover:bg-destructive/10 hover:text-destructive"
                                    aria-label="刪除對話"
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        setDeleteDialogId(conv.id)
                                    }}
                                >
                                    <Trash2 className="h-3.5 w-3.5" />
                                </Button>
                            </div>
                        </div>
                    ))}
                </div>
            </ScrollArea>


            {/* Delete Confirmation Dialog */}
            <Dialog open={!!deleteDialogId} onOpenChange={(open) => !open && setDeleteDialogId(null)}>
                <DialogContent className="sm:max-w-md bg-card border-border p-0 overflow-hidden">
                    {/* Warning Header */}
                    <div className="bg-destructive/10 px-6 py-4 border-b border-destructive/20">
                        <DialogTitle className="flex items-center gap-2 text-destructive">
                            <Trash2 className="h-5 w-5" />
                            刪除對話
                        </DialogTitle>
                    </div>

                    {/* Content */}
                    <div className="px-6 py-4">
                        <DialogDescription className="text-base text-muted-foreground">
                            確定要刪除這個對話嗎？此操作無法復原。
                        </DialogDescription>
                    </div>

                    {/* Footer */}
                    <DialogFooter className="px-6 py-4 border-t border-border bg-muted/30">
                        <Button
                            variant="outline"
                            onClick={() => setDeleteDialogId(null)}
                            disabled={deleting}
                            className="border-border"
                        >
                            取消
                        </Button>
                        <Button
                            onClick={handleDelete}
                            disabled={deleting}
                            className="bg-destructive hover:bg-destructive/90 text-destructive-foreground font-medium"
                        >
                            {deleting && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
                            刪除
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    )
}
