// src/data/db.js

const allMovies = [
  {
    id: 1,
    title: "The Grand Test",
    poster: "https://i.imgur.com/v1hG1bF.png", // Using a placeholder image
    duration: "2h 10m",
    plot_short: "A developer learns the ins and outs of testing in this thrilling coding epic.",
    plot_long: "An epic tale of one developer's journey to understand unit, integration, and end-to-end testing. Faced with legacy code and tight deadlines, they must find the courage to refactor, test, and deploy, learning valuable lessons about software craftsmanship along the way.",
    director: "Jane Doe",
    cast: ["Alex Smith", "Maria Garcia", "Chen Wei"],
    rating: 0,
    isTop: true,
  },
  {
    id: 2,
    title: "API Adventure",
    poster: "https://i.imgur.com/v1hG1bF.png",
    duration: "1h 45m",
    plot_short: "Two microservices fall in love, but a firewall stands in their way.",
    plot_long: "Set in the sprawling digital city of 'The Grid', a plucky front-end request (Req) must navigate the dangerous back-end networks to unite with its one true love, a database response (Res). They must overcome latency, 404 errors, and the tyrannical Gateway API.",
    director: "John Smith",
    cast: ["Kenji Tanaka", "Sarah B.", "David Lee"],
    rating: 0,
    isTop: true,
  },
  {
    id: 3,
    title: "CSS: The Reckoning",
    poster: "https://i.imgur.com/v1hG1bF.png",
    duration: "3h 01m",
    plot_short: "A designer struggles to center a div.",
    plot_long: "In a post-apocalyptic world where tables are used for layout, one hero emerges. Armed only with 'flexbox' and 'grid', they fight to bring balance and alignment to the web, challenging the old ways of 'float: left' and '!important' hacks.",
    director: "Ana Kova",
    cast: ["Emily White", "James Brown", "Priya Patel"],
    rating: 0,
    isTop: false,
  },
  // Add 10-15 more dummy movie objects here
  { id: 4, title: "Repo Rangers", poster: "https://i.imgur.com/v1hG1bF.png", isTop: true, duration: "1h 30m",  },
  { id: 5, title: "The Commit", poster: "https://i.imgur.com/v1hG1bF.png", isTop: true, duration: "1h 30m",  },
  { id: 6, title: "Merge Conflict", poster: "https://i.imgur.com/v1hG1bF.png", isTop: true, duration: "1h 30m",  },
  { id: 7, title: "JavaScript Jedi", poster: "https://i.imgur.com/v1hG1bF.png", isTop: true, duration: "1h 30m",  },
  { id: 8, title: "Python's Path", poster: "https://i.imgur.com/v1hG1bF.png", isTop: true, duration: "1h 30m",  },
  { id: 9, title: "The Forgotten Semicolon", poster: "https://i.imgur.com/v1hG1bF.png", isTop: true, duration: "1h 30m",  },
  { id: 10, title: "Node.js Nightmares", poster: "https://i.imgur.com/v1hG1bF.png", isTop: true, duration: "1h 30m",  },
  { id: 11, title: "Legacy Code", poster: "https://i.imgur.com/v1hG1bF.png", isTop: false, duration: "1h 30m",  },
  { id: 12, title: "Debian Dawn", poster: "https://i.imgur.com/v1hG1bF.png", isTop: false, duration: "1h 30m",  },
];

// Mimic an API call
export const useMovieApi = () => {
  const getRecommended = () => {
    return allMovies.filter(m => !m.isTop).slice(0, 10);
  };

  const getTop = () => {
    return allMovies.filter(m => m.isTop).slice(0, 10);
  };

  const getRandomBanner = () => {
    return allMovies[Math.floor(Math.random() * allMovies.length)];
  };

  const getMovieById = (id) => {
    // In a real app, this would be a fetch: /api/movies/${id}
    return allMovies.find(movie => movie.id === parseInt(id));
  };

  return { getRecommended, getTop, getRandomBanner, getMovieById };
};