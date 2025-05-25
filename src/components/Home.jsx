import React from 'react';

function Home() {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="relative h-96 mb-8 rounded-lg overflow-hidden">
        <img 
          src="https://images.pexels.com/photos/2760243/pexels-photo-2760243.jpeg"
          alt="Matériaux à changement de phase"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
          <h1 className="text-4xl font-bold text-white text-center px-4">
            Matériaux à Changement de Phase (MCP)
          </h1>
        </div>
      </div>

      <div className="prose max-w-none">
        <p className="text-lg text-gray-700 mb-8">
          Les Matériaux à Changement de Phase (MCP) sont des solutions innovantes pour le stockage d'énergie thermique,
          permettant d'améliorer l'efficacité énergétique des bâtiments et des processus industriels.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
          <div className="bg-blue-50 p-6 rounded-lg">
            <div className="h-48 mb-4 rounded-lg overflow-hidden">
              <img 
                src="https://images.pexels.com/photos/3785927/pexels-photo-3785927.jpeg"
                alt="Avantages des MCP"
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="text-xl font-semibold text-blue-900 mb-3">Avantages Clés</h3>
            <ul className="list-disc list-inside text-gray-700">
              <li>Stockage d'énergie efficace</li>
              <li>Régulation thermique passive</li>
              <li>Économies d'énergie significatives</li>
              <li>Solution écologique</li>
            </ul>
          </div>

          <div className="bg-green-50 p-6 rounded-lg">
            <div className="h-48 mb-4 rounded-lg overflow-hidden">
              <img 
                src="https://images.pexels.com/photos/1216589/pexels-photo-1216589.jpeg"
                alt="Applications des MCP"
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="text-xl font-semibold text-green-900 mb-3">Applications</h3>
            <ul className="list-disc list-inside text-gray-700">
              <li>Construction durable</li>
              <li>Transport de matériaux sensibles</li>
              <li>Systèmes de refroidissement</li>
              <li>Textile intelligent</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;