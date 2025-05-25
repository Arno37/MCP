import React from 'react';

function About() {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="relative h-64 mb-6 rounded-lg overflow-hidden">
        <img 
          src="https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg"
          alt="Technologie MCP"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
          <h2 className="text-3xl font-bold text-white">À propos des MCP</h2>
        </div>
      </div>

      <div className="prose max-w-none">
        <p className="text-lg text-gray-700 mb-6">
          Les Matériaux à Changement de Phase (MCP) sont des substances qui absorbent et libèrent de l'énergie thermique
          lors du changement de phase, généralement de l'état solide à l'état liquide et vice versa.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="h-48 mb-4 rounded-lg overflow-hidden">
              <img 
                src="https://images.pexels.com/photos/247763/pexels-photo-247763.jpeg"
                alt="Principe de fonctionnement"
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="text-xl font-semibold mb-3">Principe de Fonctionnement</h3>
            <p className="text-gray-700">
              Lors du changement de phase, les MCP peuvent stocker et libérer de grandes quantités d'énergie à température
              constante, ce qui en fait des solutions idéales pour la gestion thermique.
            </p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="h-48 mb-4 rounded-lg overflow-hidden">
              <img 
                src="https://images.pexels.com/photos/2150/sky-space-dark-galaxy.jpg"
                alt="Types de MCP"
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="text-xl font-semibold mb-3">Types de MCP</h3>
            <ul className="list-disc list-inside text-gray-700">
              <li>MCP organiques</li>
              <li>MCP inorganiques</li>
              <li>Eutectiques</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default About;