import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { AlertTriangle } from "lucide-react"

interface ErrorDialogProps {
    error: string | null
    onClose: () => void
}

export function ErrorDialog({ error, onClose }: ErrorDialogProps) {
    return (
        <Dialog open={!!error} onOpenChange={(open) => !open && onClose()}>
            <DialogContent className="sm:max-w-md bg-white p-0 overflow-hidden">
                {/* Red Error Header */}
                <div className="bg-red-500 px-6 py-4">
                    <DialogTitle className="flex items-center gap-2 text-white">
                        <AlertTriangle className="h-5 w-5" />
                        Error Occurred
                    </DialogTitle>
                </div>

                {/* White Content Area */}
                <div className="px-6 py-4 bg-white">
                    <DialogDescription className="text-base text-gray-700">
                        {error}
                    </DialogDescription>
                </div>

                {/* Footer with solid button */}
                <DialogFooter className="px-6 py-4 bg-white border-t">
                    <Button
                        onClick={onClose}
                        className="bg-gray-600 hover:bg-gray-700 text-white font-medium"
                    >
                        Close
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
