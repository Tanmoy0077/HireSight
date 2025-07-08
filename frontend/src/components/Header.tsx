import { Link, useLocation } from "react-router-dom";
import { Lightbulb, Upload, ArrowLeft } from "lucide-react";

const NAV_ITEMS_HOME = [
  { label: "Home", href: "#home" },
  { label: "Features", href: "#features" },
  { label: "About", href: "#about" },
];

const Header = () => {
  const location = useLocation();

  const renderNavLinks = () => {
    switch (location.pathname) {
      case "/":
        return (
          <div className="flex items-center gap-8">
            {NAV_ITEMS_HOME.map(({ label, href }) => (
              <a
                key={href}
                href={href}
                className="hover:text-blue-600 text-gray-700 font-medium transition"
              >
                {label}
              </a>
            ))}
          </div>
        );
      case "/upload":
        return (
          <Link
            to="/"
            className="flex items-center gap-2 text-gray-700 hover:text-blue-600 font-medium"
          >
            <ArrowLeft className="w-5 h-5" />
            Back
          </Link>
        );
      case "/dashboard":
        return (
          <Link
            to="/upload"
            className="flex items-center gap-2 text-gray-700 hover:text-blue-600 font-medium"
          >
            <Upload className="w-5 h-5" />
            Upload New
          </Link>
        );
      default:
        return null;
    }
  };

  return (
    <header className="bg-white shadow sticky top-0 z-10">
      <div className="container mx-auto px-4 flex justify-between items-center h-16">
        <Link
          to="/"
          className="font-bold text-2xl flex items-center gap-2 text-blue-600"
        >
          <Lightbulb className="w-6 h-6" />
          HireSight
        </Link>
        <nav>{renderNavLinks()}</nav>
      </div>
    </header>
  );
};

export default Header;
