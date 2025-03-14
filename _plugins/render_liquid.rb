module Jekyll
    module RenderLiquidFilter
      def render_liquid(input)
        # Parse the input string as a Liquid template.
        template = Liquid::Template.parse(input)
        # Render using the current context. The 'environments.first'
        # gives access to the Liquid context (like site data).
        template.render(@context.environments.first)
      end
    end
  end
  
  Liquid::Template.register_filter(Jekyll::RenderLiquidFilter)