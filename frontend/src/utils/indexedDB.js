// src/utils/indexedDB.js

// Define database and object store names
const dbName = "PokedexDB";
const pokemonStore = "pokemon";
const itemsStore = "items";
const pokemonFavoritesStore = "pokemonFavorites";
const itemFavoritesStore = "itemFavorites";
const teamStore = "team";

// Function to open the IndexedDB database
const openDB = () => {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(dbName, 2); // Increment version to trigger upgrade

    // Handle database upgrades
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      // Create object stores if they do not exist
      if (!db.objectStoreNames.contains(pokemonStore)) {
        db.createObjectStore(pokemonStore, { keyPath: "id" });
      }
      if (!db.objectStoreNames.contains(itemsStore)) {
        db.createObjectStore(itemsStore, { keyPath: "id" });
      }
      if (!db.objectStoreNames.contains(pokemonFavoritesStore)) {
        db.createObjectStore(pokemonFavoritesStore, { keyPath: "_id" });
      }
      if (!db.objectStoreNames.contains(itemFavoritesStore)) {
        db.createObjectStore(itemFavoritesStore, { keyPath: "_id" });
      }
      if (!db.objectStoreNames.contains(teamStore)) {
        db.createObjectStore(teamStore, { keyPath: "id" });
      }
    };

    // Resolve the promise with the database instance on success
    request.onsuccess = (event) => {
      resolve(event.target.result);
    };

    // Reject the promise with the error on failure
    request.onerror = (event) => {
      reject(event.target.error);
    };
  });
};

// Function to save Pokemon to IndexedDB
export const savePokemonToIndexedDB = async (pokemon) => {
  const db = await openDB();
  const transaction = db.transaction(pokemonStore, "readwrite");
  const store = transaction.objectStore(pokemonStore);
  pokemon.forEach((p) => store.put(p)); // Save each Pokemon to the store
  return transaction.complete;
};

// Function to get all Pokemon from IndexedDB
export const getPokemonFromIndexedDB = async () => {
  const db = await openDB();
  const transaction = db.transaction(pokemonStore, "readonly");
  const store = transaction.objectStore(pokemonStore);
  return new Promise((resolve, reject) => {
    const request = store.getAll(); // Get all Pokemon from the store
    request.onsuccess = (event) => {
      resolve(event.target.result);
    };
    request.onerror = (event) => {
      reject(event.target.error);
    };
  });
};

// Function to get a Pokemon by ID from IndexedDB
export const getPokemonByIdFromIndexedDB = async (id) => {
  const db = await openDB();
  const transaction = db.transaction(pokemonStore, "readonly");
  const store = transaction.objectStore(pokemonStore);
  return new Promise((resolve, reject) => {
    const request = store.get(parseInt(id, 10)); // Get a specific Pokemon by ID
    request.onsuccess = (event) => {
      resolve(event.target.result);
    };
    request.onerror = (event) => {
      reject(event.target.error);
    };
  });
};

// Function to save items to IndexedDB
export const saveItemsToIndexedDB = async (items) => {
  const db = await openDB();
  const transaction = db.transaction(itemsStore, "readwrite");
  const store = transaction.objectStore(itemsStore);
  items.forEach((item) => store.put(item)); // Save each item to the store
  return transaction.complete;
};

// Function to get all items from IndexedDB
export const getItemsFromIndexedDB = async () => {
  const db = await openDB();
  const transaction = db.transaction(itemsStore, "readonly");
  const store = transaction.objectStore(itemsStore);
  return new Promise((resolve, reject) => {
    const request = store.getAll(); // Get all items from the store
    request.onsuccess = (event) => {
      resolve(event.target.result);
    };
    request.onerror = (event) => {
      reject(event.target.error);
    };
  });
};

// Function to get an item by ID from IndexedDB
export const getItemByIdFromIndexedDB = async (id) => {
  const db = await openDB();
  const transaction = db.transaction(itemsStore, "readonly");
  const store = transaction.objectStore(itemsStore);
  return new Promise((resolve, reject) => {
    const request = store.get(parseInt(id, 10)); // Get a specific item by ID
    request.onsuccess = (event) => {
      resolve(event.target.result);
    };
    request.onerror = (event) => {
      reject(event.target.error);
    };
  });
};

// Function to get favorite Pokemon from IndexedDB
export const getPokemonFavoritesFromIndexedDB = async () => {
  const db = await openDB();
  const transaction = db.transaction(pokemonFavoritesStore, "readonly");
  const store = transaction.objectStore(pokemonFavoritesStore);
  return new Promise((resolve, reject) => {
    const request = store.getAll(); // Get all favorite Pokemon from the store
    request.onsuccess = (event) => {
      resolve(event.target.result);
    };
    request.onerror = (event) => {
      reject(event.target.error);
    };
  });
};

// Function to get favorite items from IndexedDB
export const getItemFavoritesFromIndexedDB = async () => {
  const db = await openDB();
  const transaction = db.transaction(itemFavoritesStore, "readonly");
  const store = transaction.objectStore(itemFavoritesStore);
  return new Promise((resolve, reject) => {
    const request = store.getAll(); // Get all favorite items from the store
    request.onsuccess = (event) => {
      resolve(event.target.result);
    };
    request.onerror = (event) => {
      reject(event.target.error);
    };
  });
};

// Function to toggle the favorite status of a Pokemon in IndexedDB
export const togglePokemonFavoriteInIndexedDB = async (_id, entity) => {
  const db = await openDB();
  const transaction = db.transaction(pokemonFavoritesStore, "readwrite");
  const store = transaction.objectStore(pokemonFavoritesStore);
  const existingFavorite = await new Promise((resolve, reject) => {
    const request = store.get(_id); // Check if the Pokemon is already a favorite
    request.onsuccess = (event) => {
      resolve(event.target.result);
    };
    request.onerror = (event) => {
      reject(event.target.error);
    };
  });

  if (existingFavorite) {
    store.delete(_id); // Remove from favorites if it already exists
    console.log(`Removed ${entity.name} from favorites`);
  } else {
    store.put({ _id, ...entity }); // Add to favorites if it does not exist
    console.log(`Added ${entity.name} to favorites`);
  }
  return transaction.complete;
};

// Function to toggle the favorite status of an item in IndexedDB
export const toggleItemFavoriteInIndexedDB = async (_id, entity) => {
  const db = await openDB();
  const transaction = db.transaction(itemFavoritesStore, "readwrite");
  const store = transaction.objectStore(itemFavoritesStore);
  const existingFavorite = await new Promise((resolve, reject) => {
    const request = store.get(_id); // Check if the item is already a favorite
    request.onsuccess = (event) => {
      resolve(event.target.result);
    };
    request.onerror = (event) => {
      reject(event.target.error);
    };
  });

  if (existingFavorite) {
    store.delete(_id); // Remove from favorites if it already exists
    console.log(`Removed ${entity.name} from favorites`);
  } else {
    store.put({ _id, ...entity }); // Add to favorites if it does not exist
    console.log(`Added ${entity.name} to favorites`);
  }
  return transaction.complete;
};

// ========== TEAM MANAGEMENT FUNCTIONS ==========

// Function to save entire team to IndexedDB
export const saveTeam = async (team) => {
  try {
    const db = await openDB();
    const transaction = db.transaction(teamStore, "readwrite");
    const store = transaction.objectStore(teamStore);

    // Clear existing team
    await new Promise((resolve, reject) => {
      const clearRequest = store.clear();
      clearRequest.onsuccess = () => resolve();
      clearRequest.onerror = () => reject(clearRequest.error);
    });

    // Add each Pokemon
    for (const pokemon of team) {
      await new Promise((resolve, reject) => {
        const addRequest = store.put(pokemon);
        addRequest.onsuccess = () => resolve();
        addRequest.onerror = () => reject(addRequest.error);
      });
    }

    return true;
  } catch (error) {
    console.error("Error saving team to IndexedDB:", error);
    return false;
  }
};

// Function to load team from IndexedDB
export const loadTeam = async () => {
  try {
    const db = await openDB();
    const transaction = db.transaction(teamStore, "readonly");
    const store = transaction.objectStore(teamStore);

    return new Promise((resolve, reject) => {
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result || []);
      request.onerror = () => reject(request.error);
    });
  } catch (error) {
    console.error("Error loading team from IndexedDB:", error);
    return [];
  }
};

// Function to add or update a single Pokemon in team
export const savePokemonToTeam = async (pokemon) => {
  try {
    const team = await loadTeam();

    // Check if Pokemon already exists in team
    const existingIndex = team.findIndex((p) => p.id === pokemon.id);

    if (existingIndex >= 0) {
      // Update existing Pokemon
      team[existingIndex] = pokemon;
    } else {
      // Add new Pokemon (max 6)
      if (team.length >= 6) {
        console.warn("Team is full (max 6 Pokemon)");
        return false;
      }
      team.push(pokemon);
    }

    return await saveTeam(team);
  } catch (error) {
    console.error("Error saving Pokemon to team:", error);
    return false;
  }
};

// Function to remove a Pokemon from team
export const removePokemonFromTeam = async (pokemonId) => {
  try {
    const team = await loadTeam();
    const filteredTeam = team.filter((p) => p.id !== pokemonId);
    return await saveTeam(filteredTeam);
  } catch (error) {
    console.error("Error removing Pokemon from team:", error);
    return false;
  }
};

// Function to clear entire team
export const clearTeam = async () => {
  try {
    const db = await openDB();
    const transaction = db.transaction(teamStore, "readwrite");
    const store = transaction.objectStore(teamStore);

    return new Promise((resolve, reject) => {
      const request = store.clear();
      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(request.error);
    });
  } catch (error) {
    console.error("Error clearing team:", error);
    return false;
  }
};
