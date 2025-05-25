import React from 'react';

function Applications() {
  const applications = [
    {
      title: "Construction",
      description: "Intégration dans les matériaux de construction pour une régulation thermique passive.",
      examples: ["Murs", "Plafonds", "Planchers chauffants"],
      image: "https://images.pexels.com/photos/159306/construction-site-build-construction-work-159306.jpeg"
    },
    {
      title: "Transport",
      description: "Protection thermique pour le transport de produits sensibles.",
      examples: ["Conteneurs réfrigérés", "Emballages isothermes", "Transport médical"],
      image: "https://images.pexels.com/photos/2199293/pexels-photo-2199293.jpeg"
    },
    {
      title: "Textile",
      description: "Vêtements et textiles techniques pour le confort thermique.",
      examples: ["Vêtements de sport", "Équipements de protection", "Literie"],
      image: "https://images.pexels.com/photos/325876/pexels-photo-325876.jpeg"
    }
  ];

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="relative h-64 mb-8 rounded-lg overflow-hidden">
        <img 
          src="https://images.pexels.com/photos/1117452/pexels-photo-1117452.jpeg"
          alt="Applications MCP"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
          <h2 className="text-3xl font-bold text-white">Applications des MCP</h2>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {applications.map((app, index) => (
          <div key={index} className="bg-gray-50 p-4 rounded-lg">
            <div className="h-48 mb-4 rounded-lg overflow-hidden">
              <img 
                src={app.image}
                alt={app.title}
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="text-xl font-semibold text-blue-900 mb-3">{app.title}</h3>
            <p className="text-gray-700 mb-4">{app.description}</p>
            <ul className="list-disc list-inside text-gray-600">
              {app.examples.map((example, i) => (
                <li key={i}>{example}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Applications;