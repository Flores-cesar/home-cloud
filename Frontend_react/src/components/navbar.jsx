import React from 'react';
import { FileText } from 'lucide-react';

const Navbar = () => {
    return (
      <nav className="sticky top-0 z-50 bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
  
            {/* Logo */}
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center 
                              bg-gradient-to-br from-sky-500 to-cyan-400">
                <FileText className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">
                DocuGroup
              </span>
            </div>
  
            {/* Menu */}
            <div className="flex items-center gap-8">
              {['Integrantes', 'Mis pagos', 'Documentos', 'Contactos', 'Uso de la app'].map(item => (
                <a
                  key={item}
                  href="#"
                  className="text-gray-600 hover:text-sky-600 transition-colors"
                >
                  {item}
                </a>
              ))}
            </div>
  
            {/* Auth */}
            <div className="flex items-center gap-3">
              <button className="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors">
                Sign in
              </button>
              <button className="px-4 py-2 rounded-lg text-white 
                                 bg-gradient-to-r from-sky-500 to-cyan-400 
                                 hover:shadow-lg hover:scale-105 transition-all">
                Register
              </button>
            </div>
  
          </div>
        </div>
      </nav>
    );
  };

export default Navbar;