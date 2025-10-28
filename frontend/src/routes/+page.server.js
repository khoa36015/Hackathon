/** @type {import('./$types').PageServerLoad} */
export async function load({ cookies }) {
  const token = cookies.get('token');
  return {
    token // truyền xuống layout và page
  };
}