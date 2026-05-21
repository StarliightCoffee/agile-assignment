import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
import { useUser } from '@/context/user-context';

function AccountOptions() {
    const { userId } = useUser()
    const navigate = useNavigate()
    const [isDialogOpen, setIsDialogOpen] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [dataLoading, setDataLoading] = useState(false)
    const [dataError, setDataError] = useState<string | null>(null)

    const handleRequestData = async () => {
        if (!userId) return
        setDataLoading(true)
        setDataError(null)
        try {
            const [nameRes, typeRes, emailRes, phoneRes, membershipRes] = await Promise.all([
                fetch(`/api/account-mgmt/get-user-name/${userId}`),
                fetch(`/api/account-mgmt/get-user-type/${userId}`),
                fetch(`/api/account-mgmt/get-user-email/${userId}`),
                fetch(`/api/account-mgmt/get-user-phone-number/${userId}`),
                fetch(`/api/account-mgmt/get-user-membership-type/${userId}`),
            ])

            if (!nameRes.ok || !typeRes.ok || !emailRes.ok || !phoneRes.ok || !membershipRes.ok) {
                setDataError('Failed to fetch account data. Please try again.')
                return
            }

            const [name, type, email, phone, membership] = await Promise.all([
                nameRes.json(),
                typeRes.json(),
                emailRes.json(),
                phoneRes.json(),
                membershipRes.json(),
            ])

            const txt = [
                'GymPro Account Data Export',
                `Generated: ${new Date().toLocaleString()}`,
                '',
                `Name:             ${name.name}`,
                `Account Type:     ${type.type}`,
                `Email:            ${email.email}`,
                `Phone Number:     ${phone.phone_number}`,
                `Membership Type:  ${membership.membership_type}`,
            ].join('\n')

            const blob = new Blob([txt], { type: 'text/plain' })
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `gympro-account-${userId}.txt`
            a.click()
            URL.revokeObjectURL(url)
        } catch {
            setDataError('Could not reach the server. Please try again.')
        } finally {
            setDataLoading(false)
        }
    }

    const handleDeleteConfirm = async () => {
        if (!userId) return
        setError(null)
        try {
            const res = await fetch(`/api/db-api/delete-user/${userId}`, { method: 'DELETE' })
            if (!res.ok) {
                setError('Failed to delete account. Please try again.')
                return
            }
            navigate('/')
        } catch {
            setError('Could not reach the server. Please try again.')
        }
    }

    return (
        <SidebarWrapper title="Account Options">
            <div className="flex flex-col gap-4 p-8 login-card-enter">
                <Button variant="default" className="w-1/4" onClick={handleRequestData} disabled={dataLoading}>
                    {dataLoading ? 'Fetching...' : 'Request your Data'}
                </Button>
                {dataError && <p className="text-sm text-destructive">{dataError}</p>}
                <Button variant="destructive" className="w-1/4" onClick={() => setIsDialogOpen(true)}>
                    Delete Account
                </Button>

                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>Delete Account</DialogTitle>
                            <DialogDescription>
                                This will permanently delete your account and all associated data. This action cannot be undone.
                            </DialogDescription>
                        </DialogHeader>
                        {error && <p className="text-sm text-destructive">{error}</p>}
                        <DialogFooter>
                            <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
                                Cancel
                            </Button>
                            <Button variant="destructive" onClick={handleDeleteConfirm}>
                                Delete my account
                            </Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>
        </SidebarWrapper>
    )
}

export default AccountOptions
