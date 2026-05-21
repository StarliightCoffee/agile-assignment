import { useState, useEffect, useCallback } from 'react';
import { SidebarWrapper } from "@/components/sidebar-wrapper";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { useUser } from '@/context/user-context';

type ParkingRecord = {
    parking_id: number
    user_id: number
    license_plate: string
    payment: number
    start_timestamp: string
    end_timestamp: string
}

function Parking() {
    const { userId } = useUser()
    const [licensePlate, setLicensePlate] = useState('')
    const [payment, setPayment] = useState('')
    const [endTime, setEndTime] = useState('')
    const [records, setRecords] = useState<ParkingRecord[]>([])
    const [error, setError] = useState<string | null>(null)

    const fetchRecords = useCallback(() => {
        if (!userId) return
        fetch(`/api/db-api/get-parking/${userId}`)
            .then(r => r.ok ? r.json() : Promise.reject())
            .then(setRecords)
            .catch(() => {})
    }, [userId])

    useEffect(() => { fetchRecords() }, [fetchRecords])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!userId) return
        setError(null)

        const body = new FormData()
        body.append('user_id', String(userId))
        body.append('license_plate', licensePlate)
        body.append('payment', payment)
        body.append('start_timestamp', new Date().toISOString())
        body.append('end_timestamp', new Date(endTime).toISOString())

        try {
            const res = await fetch('/api/db-api/insert-parking-item', { method: 'POST', body })
            if (!res.ok) {
                setError('Failed to register parking. Please try again.')
                return
            }
            setLicensePlate('')
            setPayment('')
            setEndTime('')
            fetchRecords()
        } catch {
            setError('Could not reach the server. Please try again.')
        }
    }

    return (
        <SidebarWrapper title="Parking">
            <div className="p-8 login-card-enter flex flex-col gap-8">
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <div className="flex w-full max-w-2xl items-end gap-3">
                        <div className="flex flex-col gap-2 flex-1">
                            <Label htmlFor="license-plate">License Plate</Label>
                            <Input
                                id="license-plate"
                                placeholder="AB12 CDE"
                                value={licensePlate}
                                onChange={e => setLicensePlate(e.target.value)}
                                required
                            />
                        </div>
                        <div className="flex flex-col gap-2 w-32">
                            <Label htmlFor="payment">Payment (£)</Label>
                            <Input
                                id="payment"
                                type="number"
                                min={0}
                                step={0.01}
                                placeholder="0.00"
                                value={payment}
                                onChange={e => setPayment(e.target.value)}
                                required
                            />
                        </div>
                        <div className="flex flex-col gap-2">
                            <Label htmlFor="end-time">Leaving at</Label>
                            <Input
                                id="end-time"
                                type="datetime-local"
                                value={endTime}
                                onChange={e => setEndTime(e.target.value)}
                                required
                            />
                        </div>
                        <Button type="submit" className="shrink-0">Park</Button>
                    </div>
                    {error && <p className="text-sm text-destructive">{error}</p>}
                </form>

                {records.length > 0 ? (
                    <div className="flex flex-col gap-3">
                        <h2 className="text-lg font-semibold">Parking History</h2>
                        <div className="flex flex-col gap-2 max-w-2xl">
                            {records.map(record => (
                                <Card key={record.parking_id}>
                                    <CardContent className="py-4 flex items-center justify-between">
                                        <div className="flex items-center gap-6">
                                            <span className="font-mono font-semibold text-base">{record.license_plate}</span>
                                            <span className="text-sm text-muted-foreground">
                                                {new Date(record.start_timestamp).toLocaleString()} → {new Date(record.end_timestamp).toLocaleString()}
                                            </span>
                                        </div>
                                        <span className="font-semibold">£{Number(record.payment).toFixed(2)}</span>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    </div>
                ) : (
                    <p className="text-sm text-muted-foreground">No parking history found.</p>
                )}
            </div>
        </SidebarWrapper>
    );
}

export default Parking
