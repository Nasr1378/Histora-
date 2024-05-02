from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment, File, Topic

User = get_user_model()

class ModelTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        
        # Create a topic
        self.topic = Topic.objects.create(name="Django Testing")
        
        # Create a post
        self.post = Post.objects.create(
            host=self.user,
            topic=self.topic,
            title='Test Post',
            description='Test Description'
        )
        
        # Create a comment
        self.comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            body='A test comment'
        )
        
        # Create a file
        self.file = File.objects.create(
            post=self.post,
            name='Test File',
            file_type=File.FILE_PDF,
            file='path/to/file.pdf'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.host, self.user)
        self.assertTrue(isinstance(self.post, Post))

    def test_comment_creation(self):
        self.assertEqual(self.comment.body, 'A test comment')
        self.assertEqual(self.comment.user, self.user)
        self.assertTrue(isinstance(self.comment, Comment))

    def test_file_creation(self):
        self.assertEqual(self.file.name, 'Test File')
        self.assertEqual(self.file.post, self.post)
        self.assertTrue(isinstance(self.file, File))

    def test_topic_str(self):
        self.assertEqual(str(self.topic), "Django Testing")

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_comment_str(self):
        self.assertTrue(str(self.comment).startswith('A test comment'))

    def test_file_association(self):
        self.assertEqual(self.file.post.id, self.post.id)
