'use client'

import { useState } from 'react'
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { Home, Podcasts, Email, SmartToy, Menu, Close } from '@mui/icons-material';
import InsertChartIcon from '@mui/icons-material/InsertChart';
import ListAltIcon from '@mui/icons-material/ListAlt';
import AppsIcon from '@mui/icons-material/Apps';

export default function Header() {
    // Component States
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const pathname = usePathname();

    const navItems = [
        { name: 'Home', path: '/', icon: <Home sx={{ fontSize: 20 }} /> },
        { name: 'Todo', path: '/todo', icon: <ListAltIcon fontSize="small" /> },
        { name: 'Plots', path: '/plots', icon: <InsertChartIcon fontSize="small" /> },
        { name: 'Grids', path: '/styletransfer', icon: <AppsIcon fontSize="small" /> },
        { name: 'AI Assistant', path: '/chat', icon: <SmartToy fontSize="small" /> }
    ];

    // UI View
    return (
        <>
            <header className="header-wrapper">
                <div className="header-container">
                    <div className="header-content">
                        <Link href="/" className="header-logo">
                        <Image
                                src="/logo.png" // Place your logo in public folder
                                alt="Paper with Data Logo"
                                width={40}
                                height={40}
                                className="object-contain"
                            />
                            <h1 className="text-xl font-bold font-montserrat">PAPER with DATA</h1>
                        </Link>

                     

                        <button
                            className="mobile-menu-button"
                            onClick={() => setIsMenuOpen(!isMenuOpen)}
                            aria-label="Toggle menu"
                        >
                            {isMenuOpen ? <Close className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                        </button>
                    </div>
                </div>

                <div className={`mobile-menu ${isMenuOpen ? 'translate-y-0' : '-translate-y-full'}`}>
                    {/* ... mobile menu content ... */}
                </div>
            </header>
            {isMenuOpen && <div className="mobile-menu-overlay" onClick={() => setIsMenuOpen(false)} />}
        </>
    );
}