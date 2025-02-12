export default async function handler(req: any, res: any) {
    if (req.method === 'POST') {
        const { data } = req.body;

        // const postData = async (data) => {
            try {
              const response = await fetch('/api/createvectordb', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
              });
          
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
          
              const result = await response.json();
              console.log(result);
            } catch (error) {
              console.error('There was a problem with the fetch operation:', error);
            }
        //   };
    } else {
        res.status(405).json({ message: 'Only POST requests are allowed' });
    }
}