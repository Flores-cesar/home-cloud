import React from 'react';
import { FileText } from 'lucide-react';

const Footer = () => {
    return (
      <footer className="bg-gray-900 text-gray-300 mt-auto">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
  
            {/* Logo */}
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-blue-600">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="text-lg font-semibold text-white">
                DocuGroup
              </span>
            </div>
  
            {/* Links */}
            <div className="flex items-center gap-6">
              {['Privacidad', 'Términos', 'Soporte', 'Contacto'].map(link => (
                <a key={link} href="#" className="hover:text-white transition-colors">
                  {link}
                </a>
              ))}
            </div>
  
            <div className="text-sm">
              © 2026 DocuGroup
            </div>
          </div>
        </div>
      </footer>
    );
  };

export default Footer;
