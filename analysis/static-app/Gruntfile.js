module.exports = function(grunt) {
  grunt.initConfig({
    browserify: {
      js: {
        // A single entry point for our app
        src: 'app/js/app.js',
        // Compile to a single file to add a script tag for in your HTML
        dest: 'dist/js/app.js',
      },
    },
    sass: {
      dist: {
        files: {
          'dist/css/style.css': 'app/sass/style.sass'
        }
      }
    },
    copy: {
      dist: {
        expand: true,
        cwd: './dist',
        src: ['./**'],
        dest: '../static/analysis',
      },
      app: {
        expand: true,
        cwd: './app',
        src: ['./**/*.html', './**/*.css', './**/*.png'],
        dest: '../static/analysis',
      }
    },
    watch: {
      css: {
        files: 'app/**/*.sass',
        tasks: ['sass', 'copy.dist']
      },
      js: {
        files: 'app/**/*.js',
        tasks: ['browserify', 'copy.dist']
      },
      html: {
        files: ['app/**/*.html', 'app/**/*.css', 'app/**/*.png'],
        tasks: ['copy.app']
      }
    }
  });

  // Load the npm installed tasks
  grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  

  // The default tasks to run when you type: grunt
  grunt.registerTask('default', ['browserify', 'sass', 'copy']);
  grunt.registerTask('watch', ['watch']);
};
