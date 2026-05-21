import { useState, useEffect } from 'react';
import { SidebarWrapper } from '@/components/sidebar-wrapper';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useUser } from '@/context/user-context';

const PLANS = ['Standard', 'Pro', 'Pro+'] as const
type Plan = typeof PLANS[number]

export default function Membership() {
    const { userId } = useUser()
    const [membershipType, setMembershipType] = useState<string | null>(null)
    const [targetPlan, setTargetPlan] = useState<Plan | null>(null)
    const [cardNumber, setCardNumber] = useState('')
    const [expiry, setExpiry] = useState('')
    const [cvc, setCvc] = useState('')
    const [error, setError] = useState<string | null>(null)

    const fetchMembership = () => {
        if (!userId) return
        fetch(`/api/db-api/get-user/${userId}`)
            .then(r => r.ok ? r.json() : Promise.reject())
            .then(data => setMembershipType(data.membership_type))
            .catch(() => setMembershipType('Unknown'))
    }

    useEffect(() => { fetchMembership() }, [userId])

    const resetForm = () => {
        setCardNumber('')
        setExpiry('')
        setCvc('')
        setError(null)
        setTargetPlan(null)
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!userId || !targetPlan) return
        setError(null)

        try {
            const res = await fetch('/api/db-api/pay', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    action: 'membership',
                    target_membership: targetPlan,
                    card_number: cardNumber,
                    expiry,
                    cvc,
                }),
            })

            const data = await res.json()

            if (!res.ok) {
                setError(data.error ?? 'Payment failed. Please try again.')
                return
            }

            resetForm()
            fetchMembership()
        } catch {
            setError('Could not reach the server. Please try again.')
        }
    }

    return (
        <SidebarWrapper title="Membership">
            <div className="p-8 flex flex-col gap-4 login-card-enter">
                <h1 className="text-3xl font-bold mb-4">Change or Cancel Membership</h1>
                <p>Current Membership Status: <span className="font-semibold">{membershipType ?? '...'}</span></p>

                {PLANS.map(plan => (
                    <Button
                        key={plan}
                        className="w-3/5"
                        variant="default"
                        onClick={() => setTargetPlan(plan)}
                    >
                        Change to {plan}
                    </Button>
                ))}
                <Button className="w-3/5" variant="destructive">Cancel Membership</Button>
            </div>

            <Dialog open={!!targetPlan} onOpenChange={open => { if (!open) resetForm() }}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Change to {targetPlan}</DialogTitle>
                        <DialogDescription>
                            Enter your payment details to continue.
                        </DialogDescription>
                    </DialogHeader>

                    <form className="space-y-4" onSubmit={handleSubmit}>
                        <div className="space-y-2">
                            <Label htmlFor="card-number">Card Number</Label>
                            <Input
                                id="card-number"
                                inputMode="numeric"
                                autoComplete="cc-number"
                                placeholder="1234 5678 9012 3456"
                                value={cardNumber}
                                onChange={e => setCardNumber(e.target.value)}
                                required
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="card-expiry">Expiry</Label>
                                <Input
                                    id="card-expiry"
                                    autoComplete="cc-exp"
                                    placeholder="MM/YY"
                                    value={expiry}
                                    onChange={e => setExpiry(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="card-cvc">CVC</Label>
                                <Input
                                    id="card-cvc"
                                    inputMode="numeric"
                                    autoComplete="cc-csc"
                                    placeholder="123"
                                    value={cvc}
                                    onChange={e => setCvc(e.target.value)}
                                    required
                                />
                            </div>
                        </div>

                        {error && <p className="text-sm text-destructive">{error}</p>}

                        <DialogFooter>
                            <Button type="button" variant="outline" onClick={resetForm}>
                                Cancel
                            </Button>
                            <Button type="submit">Pay & Confirm</Button>
                        </DialogFooter>
                    </form>
                </DialogContent>
            </Dialog>
        </SidebarWrapper>
    )
}
