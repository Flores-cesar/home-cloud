import React from 'react';

const Home = () => {
  return (
    <div className="max-w-7xl mx-auto px-6 py-20">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4 text-gray-900">
          Organizá documentos, pagos, recordatorios todo en un solo lugar
        </h1>
        <p className="text-xl text-gray-600">
          Tu organizador colaborativo en la nube ☁️
        </p>
      </div>

      <div className="rounded-2xl p-12 text-center bg-white shadow-lg">
        <p className="text-lg text-gray-600">
          Aquí irá el contenido del Home
        </p>
        <p className="text-sm mt-2 text-gray-400">
          (Scroll para ver el navbar sticky en acción)
        </p>
      </div>

      <div className="h-96"></div>
    </div>
  );
};

export default Home;