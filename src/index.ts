import { createItemItemsPost, getItemsItemsGet  } from './client';

async function run() {
  const response = await createItemItemsPost({
    body: {
      name: "Produto X",
      price: 100
    }
  });

  console.log(response);
}

run();

getItemsItemsGet()
  .then(console.log)
  .catch(console.error);