"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Overview" },
  { href: "/industries", label: "Industries" },
  { href: "/covid", label: "COVID Impact" },
  { href: "/about", label: "About" },
];

export function Navigation() {
  const path = usePathname();
  return (
    <nav className="border-b border-slate-200 bg-white/90 backdrop-blur sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 flex items-center justify-between h-14">
        <Link href="/" className="font-bold text-slate-900">
          🇰🇪 Kenya Employment
        </Link>
        <ul className="flex gap-1 text-sm">
          {links.map((l) => (
            <li key={l.href}>
              <Link
                href={l.href}
                className={`px-3 py-2 rounded-md transition ${
                  path === l.href
                    ? "bg-brand-50 text-brand-700 font-medium"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                {l.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}