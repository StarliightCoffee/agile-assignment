import { useState } from 'react';
import { SidebarWrapper } from "@/components/sidebar-wrapper";
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useUser } from '@/context/user-context';

function Sessions() {
    const { userId } = useUser()
    const [isDialogOpen, setIsDialogOpen] = useState(false)
    const [date, setDate] = useState('')
    const [time, setTime] = useState('')
    const [trainerId, setTrainerId] = useState('')
    const [error, setError] = useState<string | null>(null)

    const resetForm = () => {
        setDate('')
        setTime('')
        setTrainerId('')
        setError(null)
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError(null)

        const body = new FormData()
        body.append('user_id', String(userId))
        body.append('trainer_id', trainerId)
        body.append('date', `${date}T${time}`)

        try {
            const res = await fetch('/api/db-api/insert-schedule-item', { method: 'POST', body })
            if (!res.ok) {
                setError('Failed to book session. Please check the trainer ID and try again.')
                return
            }
            setIsDialogOpen(false)
            resetForm()
        } catch {
            setError('Could not reach the server. Please try again.')
        }
    }

    return (
        <SidebarWrapper title="Sessions">
            <div className="p-8 login-card-enter flex flex-col gap-4">
                <Button className="w-fit" onClick={() => setIsDialogOpen(true)}>
                    Book a Session
                </Button>
                <p className="text-sm text-muted-foreground">Your booked sessions will appear here.</p>
            </div>

            <Dialog open={isDialogOpen} onOpenChange={(open) => { setIsDialogOpen(open); if (!open) resetForm() }}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Book a Session</DialogTitle>
                        <DialogDescription>
                            Choose a date, time, and trainer for your session.
                        </DialogDescription>
                    </DialogHeader>

                    <form className="space-y-4" onSubmit={handleSubmit}>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="session-date">Date</Label>
                                <Input
                                    id="session-date"
                                    type="date"
                                    value={date}
                                    onChange={e => setDate(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="session-time">Time</Label>
                                <Input
                                    id="session-time"
                                    type="time"
                                    value={time}
                                    onChange={e => setTime(e.target.value)}
                                    required
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="trainer-id">Trainer ID</Label>
                            <Input
                                id="trainer-id"
                                type="number"
                                min={1}
                                placeholder="Enter trainer ID"
                                value={trainerId}
                                onChange={e => setTrainerId(e.target.value)}
                                required
                            />
                        </div>

                        {error && <p className="text-sm text-destructive">{error}</p>}

                        <DialogFooter>
                            <Button type="button" variant="outline" onClick={() => { setIsDialogOpen(false); resetForm() }}>
                                Cancel
                            </Button>
                            <Button type="submit">Book</Button>
                        </DialogFooter>
                    </form>
                </DialogContent>
            </Dialog>
        </SidebarWrapper>
    )
}

export default Sessions
